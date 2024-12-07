import logging

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

logger = logging.getLogger(__name__)


class CSRFExemptMixin:
    """
    A mixin that exempts the dispatch method from CSRF verification.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UpdateField:
    """
    A utility class for generating extra context dynamically.
    """

    def __init__(self, **fields):
        self.context = fields

    def get_new_values(self):
        return self.context


class BaseFactureListView(CSRFExemptMixin, ListView):
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


class BaseFactureCreateView(CSRFExemptMixin, CreateView):
    title = None
    button_text = None

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


# Base views for shared logic
class BaseFactureUpdateView(CSRFExemptMixin, UpdateView):
    title = None
    button_text = None

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


class BaseFactureDeleteView(CSRFExemptMixin, DeleteView):
    title = None
    button_text = None

    def get_extra_context(self):
        return UpdateField(title=self.title, button=self.button_text).get_new_values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


class BaseFactureDetailView(CSRFExemptMixin, DetailView):
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
