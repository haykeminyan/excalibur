import logging

import pytest
from django.contrib.auth.models import User

from apps.facture.mixins import CheckOwnerFacture
from apps.facture.models import LocalFacture, WorldFacture
from apps.facture.tests.constants import LOCAL_FACTURE, WORLD_FACTURE

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test__check_owner_local_facture_superuser(request, user, superuser):
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
    request.user = superuser

    # when
    owner = CheckOwnerFacture(model=LocalFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 1
    assert owner.get_queryset()[0].pk == 1


@pytest.mark.django_db
def test__check_owner_local_facture_user(request, user):
    user_test = User.objects.create_user(username='user_test', password='foo')

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
        owner=user_test,
    )
    facture.save()
    request.user = user

    # when
    owner = CheckOwnerFacture(model=LocalFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 0


@pytest.mark.django_db
def test__check_owner_world_facture_superuser(request, user, superuser):
    # given
    facture = WorldFacture(
        receiver=WORLD_FACTURE['receiver'],
        firm_name=WORLD_FACTURE['firm_name'],
        sku=WORLD_FACTURE['sku'],
        description=WORLD_FACTURE['description'],
        specification=WORLD_FACTURE['specification'],
        quantity=WORLD_FACTURE['quantity'],
        percent=WORLD_FACTURE['percent'],
        quantity_after_percent=WORLD_FACTURE['quantity_after_percent'],
        total_tax=WORLD_FACTURE['total_tax'],
        net_pay=WORLD_FACTURE['net_pay'],
        account_number=WORLD_FACTURE['account_number'],
        owner=user,
    )
    facture.save()
    request.user = superuser

    # when
    owner = CheckOwnerFacture(model=WorldFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 1
    assert owner.get_queryset()[0].pk == 3


@pytest.mark.django_db
def test__check_owner_world_facture_user(request, user):
    user_test = User.objects.create_user(username='user_test', password='foo')
    # given
    facture = WorldFacture(
        receiver=WORLD_FACTURE['receiver'],
        firm_name=WORLD_FACTURE['firm_name'],
        sku=WORLD_FACTURE['sku'],
        description=WORLD_FACTURE['description'],
        specification=WORLD_FACTURE['specification'],
        quantity=WORLD_FACTURE['quantity'],
        percent=WORLD_FACTURE['percent'],
        quantity_after_percent=WORLD_FACTURE['quantity_after_percent'],
        total_tax=WORLD_FACTURE['total_tax'],
        net_pay=WORLD_FACTURE['net_pay'],
        account_number=WORLD_FACTURE['account_number'],
        owner=user_test,
    )
    facture.save()
    request.user = user

    # when
    owner = CheckOwnerFacture(model=WorldFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 0
