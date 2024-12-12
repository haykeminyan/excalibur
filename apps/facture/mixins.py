import logging
from fileinput import close
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.facture.models import LocalFacture

logger = logging.getLogger(__name__)


class CSRFExemptMixin:
    """
    A mixin that exempts the dispatch method from CSRF verification.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# naxer ubrat etu tupuy function and refactor as Create Facture Mixin
class UpdateField:
    """
    A utility class for generating extra context dynamically.
    """

    def __init__(self, **fields):
        self.context = fields

    def get_new_values(self):
        return self.context


class BaseFactureListView(CSRFExemptMixin, LoginRequiredMixin, ListView):
    title = None
    button_text = None
    paginate_by = 3

    def get_queryset(self):
        search_params = self.request.GET.dict()
        queryset = super().get_queryset().select_related('owner')
        page = search_params.pop('page', None)
        if search_params:
            queryset = queryset.filter(**search_params)

        return queryset

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


class BaseFactureCreateView(CSRFExemptMixin, LoginRequiredMixin, CreateView):
	model = LocalFacture
	template_name = 'html/create_facture_local.html'
	success_url = reverse_lazy('success_url')  # Update this as needed

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		# Log the current state of the form instance
		logger.info(f"Form instance before setting owner: {form.instance.owner}")
		# Set the 'owner' to the logged-in user if not set already
		# the problem is facture.data is immutable and need use instance for any field
		if not form.instance.owner:
			form.instance.owner = self.request.user
		logger.info(f"Form instance after setting owner: {form.instance.owner}")
		return form

	def form_valid(self, form):
		# Log the form instance before save to ensure the owner is set
		logger.info(f"Form instance before save: {form.instance.owner}")

		# Ensure 'owner' is set before saving
		if not form.instance.owner:
			form.instance.owner = self.request.user

		logger.info(f"Form instance after owner set: {form.instance.owner}")
		return super().form_valid(form)

	def form_invalid(self, form):
		# Log errors for debugging
		logger.error(f"Form submission failed. Errors: {form.errors.as_json()}")

		# Log the cleaned data for context
		logger.error(f"Form cleaned data: {form.cleaned_data}")

		# Add errors to the response context for rendering in the template
		return self.render_to_response(self.get_context_data(form=form))


# Base views for shared logic
class BaseFactureUpdateView(CSRFExemptMixin, LoginRequiredMixin, UpdateView):
    title = None
    button_text = None

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context

    def form_invalid(self, form):
        # Log errors for debugging
        logger.error("Form submission failed. Errors: %s", form.errors.as_json())

        # Log the cleaned data for context
        logger.error("Form cleaned data: %s", form.cleaned_data)

        # Add errors to the response context for rendering in the template
        return self.render_to_response(self.get_context_data(form=form))


class BaseFactureDeleteView(CSRFExemptMixin, LoginRequiredMixin, DeleteView):
    title = None
    button_text = None

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context

    def form_invalid(self, form):
        # Log errors for debugging
        logger.error("Form submission failed. Errors: %s", form.errors.as_json())

        # Log the cleaned data for context
        logger.error("Form cleaned data: %s", form.cleaned_data)

        # Add errors to the response context for rendering in the template
        return self.render_to_response(self.get_context_data(form=form))


class BaseFactureDetailView(CSRFExemptMixin, LoginRequiredMixin, DetailView):
    title = None
    button_text = None
    context_object_name = 'facture'
    slug_url_kwarg = 'pk'

    def get_object(self, **kwargs):
        """
        Ensure the object is fetched or return a 404 if not found.
        """
        return get_object_or_404(self.model, pk=self.kwargs.get(self.slug_url_kwarg))

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context
