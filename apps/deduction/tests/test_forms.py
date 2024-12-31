import logging
from datetime import date

import pytest

from apps.deduction.forms import DeductionForm, get_next_deduction_number
from apps.deduction.models import Deduction

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test__get_next_deduction_number_zero():
    Deduction.objects.all().delete()
    number = get_next_deduction_number()
    assert number == int(f'{date.today().year}0001')


@pytest.mark.django_db
def test__get_next_deduction_number():
    Deduction.objects.create(number_deduction=200021)
    Deduction.objects.create(number_deduction=200022)
    number = get_next_deduction_number()
    assert number == 200023


@pytest.mark.django_db
def test__deduction_form():
    Deduction.objects.create(number_deduction=200021)
    form = DeductionForm()
    assert form.fields['number_deduction'].widget.attrs['readonly'] is True
    assert form.fields['number_deduction'].disabled is True
