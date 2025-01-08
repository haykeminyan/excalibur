import io
import logging
import os
import re
from itertools import groupby

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from django.urls import reverse

from excalibur import settings
from .tasks import generate_docx_task

from excalibur.rabbitmq_service import send_rabbitmq_message

from ..facture.parsing_docx import replace_placeholders_in_doc, set_font_size
from .constants import DEDUCTION_FIELDS
from .models import Deduction

logger = logging.getLogger(__name__)


class CheckOwnerDeduction:
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
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)

    def get_deduction(self, queryset=None):
        """
        Ensure that only objects within the restricted queryset can be accessed.
        """
        queryset = self.get_queryset() if queryset is None else queryset
        pk = self.kwargs.get(self.pk_url_kwarg)

        try:
            obj = queryset.get(pk=pk)
        except self.model.DoesNotExist:
            raise PermissionDenied('you are not an owner of this deduction!')

        return obj


class BaseDeductionListView(LoginRequiredMixin, ListView):
    context_object_name = 'deductions'
    paginate_by = 3

    def get_queryset(self):
        supplier = self.request.GET.get('supplier')
        logger.error(f"Supplier filter: {supplier}")
        queryset = super().get_queryset().select_related('owner')

        if supplier:
            queryset = queryset.filter(supplier__icontains=supplier)
            logger.debug(f"Filtered queryset: {queryset}")
        else:
            queryset = queryset.order_by('-update_time')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.request.GET.get('supplier', '')
        deductions = Deduction.objects.select_related('owner')
        if supplier:
            deductions = deductions.filter(supplier__icontains=supplier)
        deductions = deductions.order_by('supplier')

        grouped_deductions = {
            supplier: list(records)
            for supplier, records in groupby(deductions, key=lambda d: d.supplier)
        }

        logger.debug(f"Grouped deductions: {grouped_deductions}")

        grouped_items = list(grouped_deductions.items())
        paginator = Paginator(grouped_items, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['suppliers_with_deductions'] = page_obj
        context['page_obj'] = page_obj
        context['supplier_filter'] = supplier

        logger.debug(f"Context data: {context}")
        return context


class BaseDeductionCreateView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('success_url')

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Send RabbitMQ message on successful creation
        message = f"Deduction created: ID={self.object.id}, Owner={self.object.owner}"
        send_rabbitmq_message(self.model, message)

        return response


class BaseDeductionUpdateView(LoginRequiredMixin, UpdateView):
    def get_object(self, queryset=None):
        return CheckOwnerDeduction(self.model, self.request, self.kwargs).get_deduction()

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Send RabbitMQ message on successful update
        message = f"Deduction updated: ID={self.object.id}, Owner={self.object.owner}"
        send_rabbitmq_message(self.model, message)

        return response


class BaseDeductionDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self, queryset=None):
        return CheckOwnerDeduction(self.model, self.request, self.kwargs).get_deduction()

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)

        # Send RabbitMQ message on successful deletion
        message = f"Deduction deleted: ID={obj.id}, Owner={obj.owner}"
        send_rabbitmq_message(self.model, message)

        return response


class BaseDeductionDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'deduction'
    slug_url_kwarg = 'pk'

    def get_object(self, **kwargs):
        return get_object_or_404(self.model, pk=self.kwargs.get(self.slug_url_kwarg))

def download_deduction_document(request, file_name):
    # Generate the full file path based on the file name
    file_path = os.path.join('/usr/src/app/apps/deduction/static/deduction/file_templates/file_output', file_name)

    # Check if the file exists and return the file response
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    else:
        return HttpResponse("File not found.", status=404)

class BaseDeductionExportDocx(LoginRequiredMixin, View):
    local_template = 'apps/deduction/static/deduction/file_templates/file_input/Deduction_template.docx'

    # def get(self, request, *args, **kwargs):
    #     deduction_object = get_object_or_404(Deduction, pk=kwargs.get('pk'))
    #
    #     # Trigger the Celery task to generate the docx in the background
    #     task_result = generate_docx_task.delay(deduction_object.id)
    #
    #     # Wait for the result to get the file path (optional, blocking until file is ready)
    #     file_path = task_result.get()
    #
    #     # Construct the URL for downloading the file
    #     file_name = os.path.basename(file_path)
    #     download_url = reverse('apps.deduction:download_deduction_document', kwargs={'file_name': file_name})
    #     # Trigger the Celery task to generate the docx in the background
    #     generate_docx_task.delay(deduction_object.id)
    #
    #     # Return an immediate response to the user (you can show a loading page or notify the user)
    #     return HttpResponse(f"Your document is being generated. Once ready, download it from <a href='{download_url}'>here</a>.")

    def get(self, request, *args, **kwargs):
        deduction_object = get_object_or_404(Deduction, pk=kwargs.get('pk'))

        # Trigger the Celery task to generate the docx in the background
        task_result = generate_docx_task.delay(deduction_object.id)

        # Immediately respond to the user that the task has started
        return JsonResponse({'status': 'Document generation started', 'task_id': task_result.id})