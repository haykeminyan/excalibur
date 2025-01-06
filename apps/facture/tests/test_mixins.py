import logging

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse, reverse_lazy

from apps.facture.forms import LocalFactureForm, WorldFactureForm
from apps.facture.mixins import CheckOwnerFacture
from apps.facture.models import LocalFacture, WorldFacture
from apps.facture.tests.constants import LOCAL_FACTURE, WORLD_FACTURE
from apps.facture.views import (
    AddLocalFacture,
    AddWorldFacture,
    DeleteLocalFacture,
    DeleteWorldFacture,
    LocalFactureDetailView,
    LocalFactureListView,
    UpdateLocalFacture,
    UpdateWorldFacture,
    WorldFactureDetailView,
    WorldFactureListView,
)

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
    assert owner.get_queryset()[0].pk == 1

    facture = owner.get_facture()

    assert facture.pk == 1
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'create_view, create_model, create_form, create_template_name, create_success_url, create_payload',
    [
        (
            AddLocalFacture,
            LocalFacture,
            LocalFactureForm,
            'html/create_facture_local.html',
            reverse_lazy('apps.facture:local_list'),
            LOCAL_FACTURE,
        ),
        (
            AddWorldFacture,
            WorldFacture,
            WorldFactureForm,
            'html/create_facture_world.html',
            reverse_lazy('apps.facture:world_list'),
            WORLD_FACTURE,
        ),
    ],
)
def test__base_facture_create(
    factory,
    user,
    create_view,
    create_model,
    create_form,
    create_template_name,
    create_success_url,
    create_payload,
):
    # given
    facture_view = create_view()

    # then
    assert facture_view.model == create_model
    assert facture_view.form_class == create_form
    assert facture_view.template_name == create_template_name
    assert facture_view.success_url == create_success_url

    # given
    payload_deduction = create_payload

    # when
    request = factory.post(facture_view.success_url, data=payload_deduction)

    request.user = user
    facture_view.request = request
    form = facture_view.get_form()
    form.instance.owner = user

    # then
    assert form.is_valid(), 'Form validation failed'
    assert facture_view.form_valid(form)


@pytest.mark.django_db
def test__base_local_facture_update(user):
    # given
    create_facture = LocalFacture.objects.create(
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
        number_facture=LOCAL_FACTURE['number_facture'],
        owner=user,
    )

    request = RequestFactory().post(
        reverse('apps.facture:local_update', kwargs={'pk': 1}),
        LOCAL_FACTURE,
    )

    request.user = user
    # when
    owner = CheckOwnerFacture(
        model=LocalFacture,
        request=request,
        kwargs={'pk': create_facture.pk},
    )

    # then
    assert len(owner.get_queryset()) == 1
    assert owner.get_queryset()[0].pk == 1
    # when
    facture_view = UpdateLocalFacture()
    facture_view.request = request
    facture_view.kwargs = {'pk': 1}

    form = facture_view.get_form()
    assert form.is_valid() is True
    assert facture_view.form_valid(form).status_code == 302

    facture = facture_view.get_object()

    assert facture.quantity_after_percent == 500


@pytest.mark.django_db
def test__base_world_facture_update(user):
    # given
    create_facture = WorldFacture.objects.create(
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
        number_facture=WORLD_FACTURE['number_facture'],
        owner=user,
    )

    request = RequestFactory().post(
        reverse('apps.facture:world_update', kwargs={'pk': 1}),
        WORLD_FACTURE,
    )

    request.user = user
    # when
    owner = CheckOwnerFacture(
        model=WorldFacture,
        request=request,
        kwargs={'pk': create_facture.pk},
    )

    # then
    assert len(owner.get_queryset()) == 1
    assert owner.get_queryset()[0].pk == 1
    # when
    facture_view = UpdateWorldFacture()
    facture_view.request = request
    facture_view.kwargs = {'pk': 1}

    form = facture_view.get_form()
    assert form.is_valid() is True
    assert facture_view.form_valid(form).status_code == 302

    facture = facture_view.get_object()

    assert facture.quantity_after_percent == 61.5


@pytest.mark.django_db
def test__base_local_facture_delete(request, user):
    # given
    LocalFacture.objects.create(
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
        number_facture=LOCAL_FACTURE['number_facture'],
        owner=user,
    )
    request.user = user
    delete_view = DeleteLocalFacture()
    delete_view.request = request
    delete_view.kwargs = {'pk': 1}

    obj = delete_view.get_object()

    assert obj.pk == 1


@pytest.mark.django_db
def test__base_world_facture_delete(request, user):
    # given
    WorldFacture.objects.create(
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
        number_facture=WORLD_FACTURE['number_facture'],
        owner=user,
    )
    request.user = user
    delete_view = DeleteWorldFacture()
    delete_view.request = request
    delete_view.kwargs = {'pk': 1}

    obj = delete_view.get_object()

    assert obj.pk == 1


@pytest.mark.django_db
def test__base_local_facture_detail(request, user):
    # given
    LocalFacture.objects.create(
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
        number_facture=LOCAL_FACTURE['number_facture'],
        owner=user,
    )
    request.user = user
    detail_view = LocalFactureDetailView()
    detail_view.request = request
    detail_view.kwargs = {'pk': 1}

    obj = detail_view.get_object()

    assert obj.pk == 1


@pytest.mark.django_db
def test__base_world_facture_detail(request, user):
    # given
    WorldFacture.objects.create(
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
        number_facture=WORLD_FACTURE['number_facture'],
        owner=user,
    )
    request.user = user
    delete_view = WorldFactureDetailView()
    delete_view.request = request
    delete_view.kwargs = {'pk': 1}

    obj = delete_view.get_object()

    assert obj.pk == 1
