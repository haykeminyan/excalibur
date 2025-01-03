import logging

import pytest

from apps.facture.forms import (
    LocalFactureForm,
    WorldFactureForm,
    get_next_facture_number,
)
from apps.facture.models import Facture

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test__get_facture_number():
    Facture.objects.all().delete()
    initial_number = get_next_facture_number()
    assert initial_number == 20250001


@pytest.mark.django_db
@pytest.mark.parametrize('facture_form', [LocalFactureForm, WorldFactureForm])
def test__facture_form(facture_form):
    form = facture_form()
    assert form.fields['number_facture'].widget.attrs['readonly'] is True
    assert form.fields['number_facture'].disabled is True
