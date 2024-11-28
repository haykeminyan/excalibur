import json
from importlib.metadata import requires

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from excalibur.mixins import JsonRequestMixin
from .forms import LocalFactureForm, WorldFactureForm
from .models import  LocalFacture, WorldFacture
import logging

logger = logging.getLogger(__name__)

class LocalFactureListView(ListView):
    model = LocalFacture
    template_name = 'html/local_list_facture.html'
    allow_empty = False
    context_object_name = 'factures'

    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context



class WorldFactureListView(ListView):
    model = WorldFacture
    template_name = 'html/world_list_facture.html'
    allow_empty = False
    context_object_name = 'factures'

    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class LocalFactureDetailView(DetailView):
    model = LocalFacture
    template_name = 'html/detail_facture_local.html'
    allow_empty = False
    context_object_name = 'facture'
    slug_url_kwarg = 'pk'

    def get_object(self, **kwargs):
        return get_object_or_404(LocalFacture, pk = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WorldFactureDetailView(DetailView):
    model = WorldFacture
    template_name = 'html/detail_facture_world.html'
    allow_empty = False
    context_object_name = 'facture'
    slug_url_kwarg = 'pk'

    def get_object(self, **kwargs):
        return get_object_or_404(WorldFacture, pk = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(csrf_exempt, name='dispatch')
class AddLocalFacture(CreateView):
    form_class = LocalFactureForm
    model = LocalFacture
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('facture_local_list')

    extra_context = {
        'title': 'Create Local Facture'
    }


@method_decorator(csrf_exempt, name='dispatch')
class AddWorldFacture(CreateView):
    form_class = WorldFactureForm
    model = WorldFacture
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('facture_world_list')

@method_decorator(csrf_exempt, name='dispatch')
class UpdateLocalFacture(UpdateView):
    form_class = LocalFactureForm
    model = LocalFacture
    template_name = 'html/create_facture_local.html'
    success_url = reverse_lazy('facture_local_list')

    extra_context = {
        'title': 'Update Local Facture'
    }


@method_decorator(csrf_exempt, name='dispatch')
class UpdateWorldFacture(UpdateView):
    form_class = WorldFactureForm
    model = WorldFacture
    template_name = 'html/create_facture_world.html'
    success_url = reverse_lazy('facture_world_list')

