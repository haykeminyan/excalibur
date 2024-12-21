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
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render

logger = logging.getLogger(__name__)


class LocalFactureListView(BaseFactureListView):
    model = LocalFacture
    template_name = 'html/local_list_facture.html'

class WorldFactureListView(BaseFactureListView):
    model = WorldFacture
    template_name = 'html/world_list_facture.html'


class LocalFactureDetailView(BaseFactureDetailView):
    model = LocalFacture
    template_name = 'html/detail_facture_local.html'


class WorldFactureDetailView(BaseFactureDetailView):
    model = WorldFacture
    template_name = 'html/detail_facture_world.html'


class AddLocalFacture(BaseFactureCreateView):
    model = LocalFacture
    form_class = LocalFactureForm
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('apps.facture:local_list')


class AddWorldFacture(BaseFactureCreateView):
    model = WorldFacture
    form_class = WorldFactureForm
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('apps.facture:world_list')


class UpdateLocalFacture(BaseFactureUpdateView):
    model = LocalFacture
    form_class = LocalFactureForm
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('apps.facture:local_list')


class UpdateWorldFacture(BaseFactureUpdateView):
    model = WorldFacture
    form_class = WorldFactureForm
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('apps.facture:world_list')


class DeleteLocalFacture(BaseFactureDeleteView):
    model = LocalFacture
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('apps.facture:local_list')


class DeleteWorldFacture(BaseFactureDeleteView):
    model = WorldFacture
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('apps.facture:world_list')
