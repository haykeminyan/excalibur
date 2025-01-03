import logging

import pytest

from apps.facture.models import LocalFacture
from apps.facture.tests.constants import LOCAL_FACTURE

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test__save(user):
    # given
    facture = LocalFacture(
        reference=LOCAL_FACTURE['reference'],
        firm_name=LOCAL_FACTURE['firm_name'],
        address=LOCAL_FACTURE['address'],
        destination=LOCAL_FACTURE['destination'],
        quantity=LOCAL_FACTURE['quantity'],
        percent=LOCAL_FACTURE['percent'],
        quantity_after_percent=LOCAL_FACTURE['quantity_after_percent'],
        tax_ht=LOCAL_FACTURE['tax_ht'],
        total_tax=LOCAL_FACTURE['total_tax'],
        total_ttc=LOCAL_FACTURE['total_ttc'],
        deposit=LOCAL_FACTURE['deposit'],
        net_pay=LOCAL_FACTURE['net_pay'],
        owner=user,
    )
    facture.save()

    # when
    saved_facture = LocalFacture.objects.get(pk=facture.pk)

    # then
    assert saved_facture.owner == user
    assert saved_facture.reference == LOCAL_FACTURE['reference']
    assert saved_facture.address == LOCAL_FACTURE['address']
    assert saved_facture.firm_name == LOCAL_FACTURE['firm_name']
    assert saved_facture.quantity == LOCAL_FACTURE['quantity']
    assert saved_facture.percent == LOCAL_FACTURE['percent']
    assert saved_facture.quantity_after_percent == LOCAL_FACTURE['quantity_after_percent']
    assert saved_facture.total_tax == LOCAL_FACTURE['total_tax']
    assert saved_facture.net_pay == LOCAL_FACTURE['net_pay']


@pytest.mark.django_db
def test__save_without_owner(user):
    # Create the LocalFacture instance without an owner
    facture = LocalFacture(
        reference=LOCAL_FACTURE['reference'],
        firm_name=LOCAL_FACTURE['firm_name'],
        address=LOCAL_FACTURE['address'],
        destination=LOCAL_FACTURE['destination'],
        quantity=LOCAL_FACTURE['quantity'],
        percent=LOCAL_FACTURE['percent'],
        quantity_after_percent=LOCAL_FACTURE['quantity_after_percent'],
        tax_ht=LOCAL_FACTURE['tax_ht'],
        total_tax=LOCAL_FACTURE['total_tax'],
        total_ttc=LOCAL_FACTURE['total_ttc'],
        deposit=LOCAL_FACTURE['deposit'],
        net_pay=LOCAL_FACTURE['net_pay'],
    )
    facture.user = user
    facture.save()

    # when
    saved_facture = LocalFacture.objects.get(pk=facture.pk)

    # then
    assert saved_facture.owner == user
    assert saved_facture.reference == LOCAL_FACTURE['reference']
    assert saved_facture.address == LOCAL_FACTURE['address']
    assert saved_facture.firm_name == LOCAL_FACTURE['firm_name']
    assert saved_facture.quantity == LOCAL_FACTURE['quantity']
    assert saved_facture.percent == LOCAL_FACTURE['percent']
    assert saved_facture.quantity_after_percent == LOCAL_FACTURE['quantity_after_percent']
    assert saved_facture.total_tax == LOCAL_FACTURE['total_tax']
    assert saved_facture.net_pay == LOCAL_FACTURE['net_pay']
