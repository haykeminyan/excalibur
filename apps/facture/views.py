import logging

from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import LocalFactureForm, WorldFactureForm
from .mixins import (
    BaseFactureCreateView,
    BaseFactureDeleteView,
    BaseFactureDetailView,
    BaseFactureListView,
    BaseFactureUpdateView,
)
from .models import LocalFacture, WorldFacture

logger = logging.getLogger(__name__)


class LocalFactureListView(BaseFactureListView):
    model = LocalFacture
    template_name = 'html/local_list_facture.html'
    context_object_name = 'factures'


class WorldFactureListView(BaseFactureListView):
    model = WorldFacture
    template_name = 'html/world_list_facture.html'
    context_object_name = 'factures'


class LocalFactureDetailView(BaseFactureDetailView):
    model = LocalFacture
    template_name = 'html/detail_facture_local.html'
    title = 'Local Facture Details'
    button_text = 'Return'


class WorldFactureDetailView(BaseFactureDetailView):
    model = WorldFacture
    template_name = 'html/detail_facture_world.html'
    title = 'World Facture Details'
    button_text = 'Return'


class AddLocalFacture(BaseFactureCreateView):
    form_class = LocalFactureForm
    model = LocalFacture
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('facture_local_list')
    title = 'Create Local Facture'
    button_text = 'Submit'


class AddWorldFacture(BaseFactureCreateView):
    form_class = WorldFactureForm
    model = WorldFacture
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('facture_world_list')
    title = 'Create World Facture'
    button_text = 'Submit'


class UpdateLocalFacture(BaseFactureUpdateView):
    form_class = LocalFactureForm
    model = LocalFacture
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('facture_local_list')
    title = 'Update Local Facture'
    button_text = 'Submit'


class UpdateWorldFacture(UpdateView):
    form_class = WorldFactureForm
    model = WorldFacture
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('facture_world_list')
    title = 'Update World Facture'
    button_text = 'Submit'


class DeleteLocalFacture(BaseFactureDeleteView):
    model = LocalFacture
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('facture_local_list')
    title = 'Delete Local Facture'
    button_text = 'Delete'


class DeleteWorldFacture(BaseFactureDeleteView):
    model = WorldFacture
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('facture_world_list')
    title = 'Delete World Facture'
    button_text = 'Delete'
