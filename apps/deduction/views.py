import logging

from django.urls import reverse_lazy

from .forms import DeductionForm
from .mixins import (
    BaseDeductionCreateView,
    BaseDeductionDeleteView,
    BaseDeductionDetailView,
    BaseDeductionListView,
    BaseDeductionUpdateView,
)
from .models import Deduction

logger = logging.getLogger(__name__)


class DeductionListView(BaseDeductionListView):
    model = Deduction
    template_name = 'html/list_deduction.html'


class DeductionDetailView(BaseDeductionDetailView):
    model = Deduction
    template_name = 'html/detail_deduction.html'


class AddDeduction(BaseDeductionCreateView):
    model = Deduction
    form_class = DeductionForm
    template_name = 'html/create_deduction.html'
    success_url = reverse_lazy('apps.deduction:list')


class UpdateDeduction(BaseDeductionUpdateView):
    model = Deduction
    form_class = DeductionForm
    template_name = 'html/create_deduction.html'
    success_url = reverse_lazy('apps.deduction:list')


class DeleteDeduction(BaseDeductionDeleteView):
    model = Deduction
    template_name = 'html/create_deduction.html'
    success_url = reverse_lazy('apps.deduction:list')
