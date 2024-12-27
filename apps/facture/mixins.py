import io
import logging
import os
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from docx import Document

from excalibur import settings
from .constants import LOCAL_FIELDS, WORLD_FIELDS
from .models import LocalFacture, WorldFacture
from .parsing_docx import replace_placeholders_in_doc, set_font_size
from django.utils.translation import get_language

logger = logging.getLogger(__name__)



class CSRFExemptMixin:
    """
    A mixin that exempts the dispatch method from CSRF verification.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BaseFactureListView(LoginRequiredMixin, ListView):
    context_object_name = 'factures'
    paginate_by = 3

    def get_queryset(self):
        search_params = self.request.GET.dict()
        queryset = super().get_queryset().select_related('owner')
        search_params.pop('page', None)
        if 'language' in search_params:
            del search_params['language']
        if search_params:
            queryset = queryset.filter(**search_params)
        else:
            queryset = queryset.order_by('-update_time')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = get_language()  # Get current language code
        context['redirect_to'] = self.request.path  # Save the current URL to redirect after language change
        return context


class BaseFactureCreateView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('success_url')  # Update this as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Log the current state of the form instance
        logger.info(f'Form instance before setting owner: {form.instance.owner}')
        # Set the 'owner' to the logged-in user if not set already
        # the problem is facture.data is immutable and need use instance for any field
        if not form.instance.owner:
            form.instance.owner = self.request.user
        logger.info(f'Form instance after setting owner: {form.instance.owner}')
        return form

    def form_valid(self, form):
        # Log the form instance before save to ensure the owner is set
        logger.info(f'Form instance before save: {form.instance.owner}')

        # Ensure 'owner' is set before saving
        if not form.instance.owner:
            form.instance.owner = self.request.user

        logger.info(f'Form instance after owner set: {form.instance.owner}')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Log errors for debugging
        logger.error(f'Form submission failed. Errors: {form.errors.as_json()}')

        # Log the cleaned data for context
        logger.error(f'Form cleaned data: {form.cleaned_data}')

        # Add errors to the response context for rendering in the template
        return self.render_to_response(self.get_context_data(form=form))


# Base views for shared logic
class BaseFactureUpdateView(LoginRequiredMixin, UpdateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Log the form instance before save to ensure the owner is set
        logger.info(f'Form instance before save: {form.instance.owner}')

        # Ensure 'owner' is set before saving
        if not form.instance.owner:
            form.instance.owner = self.request.user

        logger.info(f'Form instance after owner set: {form.instance.owner}')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Log errors for debugging
        logger.error('Form submission failed. Errors: %s', form.errors.as_json())

        # Log the cleaned data for context
        logger.error('Form cleaned data: %s', form.cleaned_data)

        # Add errors to the response context for rendering in the template
        return self.render_to_response(self.get_context_data(form=form))


class BaseFactureDeleteView(LoginRequiredMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        # Log errors for debugging
        logger.error('Form submission failed. Errors: %s', form.errors.as_json())

        # Log the cleaned data for context
        logger.error('Form cleaned data: %s', form.cleaned_data)

        # Add errors to the response context for rendering in the template
        return self.render_to_response(self.get_context_data(form=form))


class BaseFactureDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'facture'
    slug_url_kwarg = 'pk'

    def get_object(self, **kwargs):
        """
        Ensure the object is fetched or return a 404 if not found.
        """
        return get_object_or_404(self.model, pk=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
        return response