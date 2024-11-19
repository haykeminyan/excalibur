import json
from importlib.metadata import requires

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from excalibur.mixins import JsonRequestMixin
from .check_facture_type import get_facture_form, handle_facture_form, render_form_response
from .models import  LocalFacture, WorldFacture
import logging

logger = logging.getLogger(__name__)

class LocalFactureListView(ListView):
    def get(self, request, *args, **kwargs):
        facture = LocalFacture.objects.select_related('owner').all()
        return render(request, 'html/local-list-facture.html', {'facture': facture})


class WorldFactureListView(ListView):
    def get(self, request, *args, **kwargs):
        facture = WorldFacture.objects.select_related('owner').all()
        return render(request, 'html/world-list-facture.html', {'facture': facture})



@method_decorator(csrf_exempt, name='dispatch')
class FactureCreateView(JsonRequestMixin, ListView):
    def get(self, request, *args, **kwargs):
        facture_type = request.GET.get('facture_type')
        facture_form = get_facture_form(facture_type=facture_type, data=request.data)

        if facture_form:
            return render_form_response(request=request, facture_form=facture_form, facture_type=facture_type)

        return JsonResponse({'error': 'Invalid facture type'}, status=400)

    def post(self, request):
        facture_type = request.data.get('facture_type')
        facture_form = get_facture_form(facture_type=facture_type, data=request.data)
        if facture_form:
            return handle_facture_form(facture_form)
        return JsonResponse({'error': 'Invalid facture type'}, status=400)
