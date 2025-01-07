import io
import logging
import os
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from docx import Document

from excalibur.rabbitmq_service import send_rabbitmq_message

from .constants import LOCAL_FIELDS, WORLD_FIELDS
from .models import LocalFacture, WorldFacture
from .parsing_docx import replace_placeholders_in_doc, set_font_size

logger = logging.getLogger(__name__)


class CheckOwnerFacture:
    def __init__(self, model, request, kwargs, pk_url_kwarg='pk'):
        self.model = model
        self.request = request
        self.kwargs = kwargs
        self.pk_url_kwarg = pk_url_kwarg

    def get_queryset(self):
        """
        If user is superuser he can delete concrete deduction
        """
        if self.request.user.is_superuser:
            # Superuser can access all Deductions
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)

    def get_facture(self, queryset=None):
        """
        Ensure that only objects within the restricted queryset can be accessed.
        """
        queryset = self.get_queryset() if queryset is None else queryset
        pk = self.kwargs.get(self.pk_url_kwarg)

        # Attempt to get the object and handle ownership validation
        try:
            obj = queryset.get(pk=pk)
        except self.model.DoesNotExist:
            raise PermissionDenied('you are not an owner of this facture!')

        return obj


class BaseFactureListView(LoginRequiredMixin, ListView):
    context_object_name = 'factures'
    paginate_by = 3

    def get_queryset(self):
        search_params = self.request.GET.dict()
        queryset = super().get_queryset().select_related('owner')
        search_params.pop('page', None)
        if search_params:
            queryset = queryset.filter(**search_params)
        else:
            queryset = queryset.order_by('-update_time')

        return queryset


class BaseFactureCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        # Log the form instance before save to ensure the owner is set
        logger.info(f'Form instance before save: {form.instance.owner}')

        # Ensure 'owner' is set before saving
        if not form.instance.owner:
            form.instance.owner = self.request.user

        # Send RabbitMQ message on successful creation
        message = f"Facture created: ID={form.instance.pk}, Owner={form.instance.owner}"
        send_rabbitmq_message(self.model, message)

        logger.info(f'Form instance after owner set: {form.instance.owner}')
        return super().form_valid(form)


# Base views for shared logic
class BaseFactureUpdateView(LoginRequiredMixin, UpdateView):
    def get_object(self, queryset=None):
        """
        Enforce ownership validation when retrieving the object.
        """
        return CheckOwnerFacture(self.model, self.request, self.kwargs).get_facture()

    def form_valid(self, form):
        # Log the form instance before save to ensure the owner is set
        logger.info(f'Form instance before save: {form.instance.owner}')

        # Ensure 'owner' is set before saving
        if not form.instance.owner:
            form.instance.owner = self.request.user

        # Send RabbitMQ message on successful creation
        message = f"Facture updated: ID={form.instance.pk}, Owner={form.instance.owner}"
        send_rabbitmq_message(self.model, message)

        logger.info(f'Form instance after owner set: {form.instance.owner}')
        return super().form_valid(form)


class BaseFactureDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self, queryset=None):
        """
        Enforce ownership validation when retrieving the object.
        """
        return CheckOwnerFacture(self.model, self.request, self.kwargs).get_facture()

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        # Send RabbitMQ message on successful deletion
        message = f"Facture deleted: ID={self.object.id}, Owner={self.object.owner}"
        send_rabbitmq_message(self.model, message)

        return response


class BaseFactureDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'facture'
    slug_url_kwarg = 'pk'

    def get_object(self, **kwargs):
        """
        Ensure the object is fetched or return a 404 if not found.
        """
        return get_object_or_404(self.model, pk=self.kwargs.get(self.slug_url_kwarg))


class BaseFactureLocalExportDocx(LoginRequiredMixin, View):
    local_template = 'facture/file_templates/file_input/Facture_template_Maroc.docx'

    def generate_docx(self, facture_object, template_path):
        """
        Generate a DOCX file from the template and return it as a BytesIO stream.
        """
        facture_dict = model_to_dict(facture_object)
        template_path = finders.find(template_path)
        doc = Document(template_path)

        for field in LOCAL_FIELDS:
            regex = re.compile(rf'{re.escape(field)}')
            replace_placeholders_in_doc(doc, regex, facture_dict)

        set_font_size(doc)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        return file_stream

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to generate the DOCX file and return it as a downloadable response.
        """
        # Fetch deduction object
        facture_object = get_object_or_404(LocalFacture, pk=kwargs.get('pk'))

        # Generate the DOCX file
        file_stream = self.generate_docx(facture_object, self.local_template)

        file_path = f'/usr/src/app/apps/facture/static/facture/file_templates/file_output/local_facture_{facture_object.number_facture}.docx'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Save the generated DOCX file to the specified path
        with open(file_path, 'wb') as docx_file:
            docx_file.write(file_stream.getvalue())  # Assuming file_stream is a BytesIO object

        # Create the HTTP response for file download
        response = HttpResponse(
            file_stream,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = (
            f'attachment; filename="local_facture_{facture_object.number_facture}.docx"'
        )

        # Send RabbitMQ message on document export
        message = f"Local Facture document exported: ID={facture_object.id}, Owner={facture_object.owner}"
        send_rabbitmq_message(LocalFacture, message)

        return response


class BaseFactureWorldExportDocx(LoginRequiredMixin, View):
    local_template = 'facture/file_templates/file_input/Facture_template_World.docx'

    def generate_docx(self, facture_object, template_path):
        """
        Generate a DOCX file from the template and return it as a BytesIO stream.
        """
        facture_dict = model_to_dict(facture_object)
        template_path = finders.find(template_path)
        doc = Document(template_path)

        for field in WORLD_FIELDS:
            regex = re.compile(rf'{re.escape(field)}')
            replace_placeholders_in_doc(doc, regex, facture_dict)

        set_font_size(doc)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        return file_stream

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to generate the DOCX file and return it as a downloadable response.
        """
        # Fetch deduction object
        facture_object = get_object_or_404(WorldFacture, pk=kwargs.get('pk'))

        # Generate the DOCX file
        file_stream = self.generate_docx(facture_object, self.local_template)

        file_path = f'/usr/src/app/apps/facture/static/facture/file_templates/file_output/world_facture_{facture_object.number_facture}.docx'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Save the generated DOCX file to the specified path
        with open(file_path, 'wb') as docx_file:
            docx_file.write(file_stream.getvalue())  # Assuming file_stream is a BytesIO object

        # Create the HTTP response for file download
        response = HttpResponse(
            file_stream,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = (
            f'attachment; filename="world_facture_{facture_object.number_facture}.docx"'
        )

        # Send RabbitMQ message on document export
        message = f"World Facture document exported: ID={facture_object.id}, Owner={facture_object.owner}"
        send_rabbitmq_message(WorldFacture, message)

        return response
