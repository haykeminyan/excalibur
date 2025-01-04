import logging

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from apps.facture.mixins import CheckOwnerFacture
from apps.facture.models import LocalFacture, WorldFacture
from apps.facture.tests.constants import LOCAL_FACTURE, WORLD_FACTURE
from apps.facture.views import LocalFactureListView, WorldFactureListView

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test__check_owner_local_facture_superuser(request, user, superuser):
    # given
    facture = LocalFacture.objects.create(
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
    request.user = superuser

    # when
    owner = CheckOwnerFacture(model=LocalFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 1
    assert owner.get_queryset()[0].pk == 1

    facture = owner.get_facture()

    assert facture.pk == 1
    assert facture.reference == LOCAL_FACTURE['reference']
    assert facture.firm_name == LOCAL_FACTURE['firm_name']
    assert facture.address == LOCAL_FACTURE['address']
    assert facture.destination == LOCAL_FACTURE['destination']
    assert facture.quantity == LOCAL_FACTURE['quantity']
    assert facture.percent == LOCAL_FACTURE['percent']
    assert facture.quantity_after_percent == LOCAL_FACTURE['quantity_after_percent']
    assert facture.tax_ht == LOCAL_FACTURE['tax_ht']
    assert facture.total_tax == LOCAL_FACTURE['total_tax']
    assert facture.total_ttc == LOCAL_FACTURE['total_ttc']
    assert facture.deposit == LOCAL_FACTURE['deposit']
    assert facture.net_pay == LOCAL_FACTURE['net_pay']
    assert facture.owner.username == user.username


@pytest.mark.django_db
def test__check_owner_local_facture_user(request, user):
    user_test = User.objects.create_user(username='user_test', password='foo')

    # given
    facture = LocalFacture.objects.create(
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
    request.user = user

    # when
    owner = CheckOwnerFacture(model=LocalFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 0

    with pytest.raises(PermissionDenied, match='you are not an owner of this facture!'):
        owner.get_facture()


@pytest.mark.django_db
def test__check_owner_world_facture_superuser(request, user, superuser):
    # given
    facture = WorldFacture.objects.create(
        receiver=WORLD_FACTURE['receiver'],
        firm_name=WORLD_FACTURE['firm_name'],
        address=WORLD_FACTURE['address'],
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
    request.user = superuser

    # when
    owner = CheckOwnerFacture(model=WorldFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 1
    assert owner.get_queryset()[0].pk == 3

    facture = owner.get_facture()

    assert facture.pk == 3
    assert facture.receiver == WORLD_FACTURE['receiver']
    assert facture.firm_name == WORLD_FACTURE['firm_name']
    assert facture.address == WORLD_FACTURE['address']
    assert facture.sku == WORLD_FACTURE['sku']
    assert facture.description == WORLD_FACTURE['description']
    assert facture.specification == WORLD_FACTURE['specification']
    assert facture.quantity == WORLD_FACTURE['quantity']
    assert facture.quantity_after_percent == WORLD_FACTURE['quantity_after_percent']
    assert facture.total_tax == WORLD_FACTURE['total_tax']
    assert facture.net_pay == WORLD_FACTURE['net_pay']
    assert facture.account_number == WORLD_FACTURE['account_number']
    assert facture.owner.username == user.username


@pytest.mark.django_db
def test__check_owner_world_facture_user(request, user):
    user_test = User.objects.create_user(username='user_test', password='foo')
    # given
    facture = WorldFacture.objects.create(
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
    request.user = user

    # when
    owner = CheckOwnerFacture(model=WorldFacture, request=request, kwargs={'pk': facture.pk})

    # then
    assert len(owner.get_queryset()) == 0

    with pytest.raises(PermissionDenied, match='you are not an owner of this facture!'):
        owner.get_facture()


@pytest.mark.django_db
@pytest.mark.parametrize('filtering_field', [f'?deposit={LOCAL_FACTURE['deposit']}', None])
def test__base_local_facture_list(factory, user, filtering_field):
    # given
    facture_one = LocalFacture.objects.create(
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
        number_facture=LOCAL_FACTURE['number_facture'],
    )

    facture_two = LocalFacture.objects.create(
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
        deposit=LOCAL_FACTURE['deposit'] + 1,
        net_pay=LOCAL_FACTURE['net_pay'],
        owner=user,
        number_facture=LOCAL_FACTURE['number_facture'] + 1,
    )

    request = factory.get(filtering_field)
    request.user = user

    # when
    facture_list = LocalFactureListView()
    assert facture_list.context_object_name == 'factures'
    assert facture_list.paginate_by == 3
    facture_list.request = request

    query = facture_list.get_queryset()
    if filtering_field:
        assert query.count() == 1
        assert query.first() == facture_one
    else:
        assert query.count() == 2
        assert query.first() == facture_two
        assert list(query) == list(LocalFacture.objects.order_by('-update_time'))


@pytest.mark.django_db
@pytest.mark.parametrize(
    'filtering_field',
    [f'?account_number={WORLD_FACTURE['account_number']}', None],
)
def test__base_world_facture_list(factory, user, filtering_field):
    # given
    facture_one = WorldFacture.objects.create(
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
        number_facture=WORLD_FACTURE['number_facture'],
    )

    facture_two = WorldFacture.objects.create(
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
        account_number=WORLD_FACTURE['account_number'] + 1,
        owner=user,
        number_facture=WORLD_FACTURE['number_facture'] + 1,
    )

    request = factory.get(filtering_field)
    request.user = user

    # when
    facture_list = WorldFactureListView()
    assert facture_list.context_object_name == 'factures'
    assert facture_list.paginate_by == 3
    facture_list.request = request

    query = facture_list.get_queryset()
    if filtering_field:
        assert query.count() == 1
        assert query.first() == facture_one
    else:
        assert query.count() == 2
        assert query.first() == facture_two
        assert list(query) == list(WorldFacture.objects.order_by('-update_time'))
