import io
import logging
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from docx import Document


from .parsing_docx import replace_placeholders_in_doc, set_font_size

logger = logging.getLogger(__name__)

ARRAY_OF_FIELDS = [
    'number_facture',
    'address',
    'owner',
    'date',
    'firm_name',
    'update_time',
    'reference',
    'destination',
    'net_pay',
    'quantity_after_percent',
    'quantity',
    'percent',
    'deposit',
    'tax_ht',
    'total_tax',
    'total_sum_fr',
    'total_ttc',
    'contract_date',
    'account_number',
]


class CSRFExemptMixin:
    """
    A mixin that exempts the dispatch method from CSRF verification.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BaseFactureListView(CSRFExemptMixin, LoginRequiredMixin, ListView):
    context_object_name = 'factures'
    paginate_by = 3

    def get_queryset(self):
        search_params = self.request.GET.dict()
        queryset = super().get_queryset().select_related('owner')
        search_params.pop('page', None)
        if search_params:
            queryset = queryset.filter(**search_params)
        else:
            queryset = queryset.order_by('-date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BaseFactureCreateView(CSRFExemptMixin, LoginRequiredMixin, CreateView):
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
class BaseFactureUpdateView(CSRFExemptMixin, LoginRequiredMixin, UpdateView):

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


class BaseFactureDeleteView(CSRFExemptMixin, LoginRequiredMixin, DeleteView):

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


class BaseFactureDetailView(CSRFExemptMixin, LoginRequiredMixin, DetailView):
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


class BaseFactureExportDocx(BaseFactureDetailView):
    def get_facture(self, pk):
        """
        Fetch the facture object based on the provided pk (primary key).
        """
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to generate the DOCX file and return it as a downloadable response.
        """
        # Fetch facture object and prepare the replace_dict as before
        facture_object = self.get_facture(kwargs.get('pk'))
        facture_dict = model_to_dict(facture_object)

        # Load the DOCX template
        template_path = finders.find(
            'facture/file_templates/file_input/Facture_template_Maroc.docx',
        )
        doc = Document(template_path)

        # Regex for placeholder matching with boundaries
        # (handles optional spaces inside the curly braces)
        for field in ARRAY_OF_FIELDS:
            # Using \s* to match optional spaces inside the {{field}} placeholders
            # Add word boundaries to ensure we match the entire placeholder exactly
            regex = re.compile(rf'{re.escape(field)}')  # Matches {{field}} or {{ field }}

            # Replace placeholders in the document
            replace_placeholders_in_doc(doc, regex, facture_dict)
        set_font_size(doc)

        # Save the document to a BytesIO stream (in-memory file)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)  # Reset the pointer to the start of the file stream

        # Create the HTTP response for file download
        response = HttpResponse(
            file_stream,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = (
            f'attachment; filename="facture_{facture_object.pk}.docx"'
        )

        return response
