import io
import logging
from unittest.mock import Mock, mock_open, patch

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse

from apps.deduction.mixins import BaseDeductionExportDocx
from apps.deduction.models import Deduction
from apps.deduction.tests.constants import PAYLOAD_DEDUCTION_CREATE
from apps.deduction.views import (
    AddDeduction,
    DeductionDetailView,
    DeductionListView,
    DeleteDeduction,
    UpdateDeduction,
)

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.parametrize('supplier', ['foo', ''])
def test__base_deduction_list_queryset(supplier):
    # given
    Deduction.objects.create(number_deduction='20230001', supplier=supplier)
    deduction_view = DeductionListView()

    # when
    request = RequestFactory().get(reverse('apps.deduction:list'))
    deduction_view.request = request
    request.GET = {'supplier': supplier}
    queryset = deduction_view.get_queryset()

    # then
    assert len(queryset) == 1
    if supplier:
        assert queryset[0].supplier == 'foo'
    else:
        assert queryset[0].supplier == ''


@pytest.mark.django_db
def test__base_deduction_list_context_data():
    # given
    Deduction.objects.create(number_deduction='20230001', supplier='foo')
    Deduction.objects.create(number_deduction='20230002', supplier='foo')
    Deduction.objects.create(number_deduction='20230003', supplier='foo')
    Deduction.objects.create(number_deduction='20230004', supplier='foo')

    deduction_view = DeductionListView()

    # when
    request = RequestFactory().get(reverse('apps.deduction:list'))
    deduction_view.request = request
    request.GET = {'supplier': 'foo'}
    deduction_view.kwargs = {'page': 1}
    object_list = deduction_view.get_queryset()
    context_data = deduction_view.get_context_data(object_list=object_list)

    # then
    assert context_data['is_paginated'] is True

    # because parameter paginate_by in mixins.py is 3
    assert len(context_data['object_list']) == 3
    assert context_data['supplier_filter'] == 'foo'


@pytest.mark.django_db
@pytest.mark.parametrize(
    'payload_deduction',
    [
        PAYLOAD_DEDUCTION_CREATE,  # Valid payload
        {},
    ],
)
@pytest.mark.parametrize(
    'deduction_view, url',
    [
        (AddDeduction(), 'apps.deduction:create'),
        (UpdateDeduction(), 'apps.deduction:edit'),
    ],
)
def test_base_deduction_create_update_context_data(user, payload_deduction, deduction_view, url):
    """
    Test the `BaseDeductionCreateView` to check that the form handling
    and context data are working as expected, especially checking for the `owner`
    field that is set to the logged-in user.
    """
    url_kwargs = {'pk': 1} if isinstance(deduction_view, UpdateDeduction) else {}
    request = RequestFactory().post(reverse(url, kwargs=url_kwargs), payload_deduction)

    # Attach the user to the request
    request.user = user

    # Create the view instance
    view = deduction_view
    view.request = request

    # Simulate form handling
    form = view.get_form()

    # If there's payload data, validate the form
    if payload_deduction:
        form.is_valid()

        # When: Call form_valid to simulate successful form submission and object creation
        response = view.form_valid(form)

        # Get the context data after form is valid
        context_data = view.get_context_data()

        # Then: Ensure that the context includes the form and check if form is valid
        assert response.status_code == 302  # Redirect after valid form submission
        assert 'form' in context_data
        assert context_data['form'].is_valid()

        # And: Ensure that the newly created Deduction object is available in the context (self.object)
        assert view.object is not None  # This should be set after form_valid()
        assert isinstance(view.object, Deduction)  # Ensure it's an instance of Deduction
        assert (
            view.object.number_deduction == '20250001'
        )  # Ensure the Deduction object has the correct number
    else:
        # Testing invalid case where the form should fail
        assert view.form_invalid(form)
        assert 'This field is required.' == list(form.errors.values())[0][0]


@pytest.mark.django_db
def test_deduction_delete_view(superuser, user):
    # Create a test Deduction object
    deduction = Deduction.objects.create(
        number_deduction='20240002',
        owner=user,
    )

    # Define the URL for the delete view
    url = reverse('apps.deduction:delete', kwargs={'pk': deduction.pk})

    # Create the request and attach the user
    request = RequestFactory().post(url)
    request.user = superuser
    # Create the view instance
    view = DeleteDeduction()
    view.request = request
    view.kwargs = {'pk': deduction.pk}

    # Call the view's delete method
    response = view.delete(request, pk=deduction.pk)

    # Assert that the deduction object was deleted
    assert response.status_code == 302  # Redirection after successful deletion
    assert not Deduction.objects.filter(pk=deduction.pk).exists()  # Ensure the object is deleted


@pytest.mark.django_db
def test_deduction_delete_view_invalid_user(user):
    # Create a test Deduction object
    owner = User.objects.create(username='owner', password='password')
    deduction = Deduction.objects.create(
        number_deduction='20250001',
        owner=owner,
    )

    # Define the URL for the delete view
    url = reverse('apps.deduction:delete', kwargs={'pk': deduction.pk})

    # Create the request and attach a different user
    request = RequestFactory().post(url)
    request.user = user  # incorrect user

    # Create the view instance
    view = DeleteDeduction()
    view.request = request

    view.kwargs = {'pk': deduction.pk}

    # Verify that a PermissionDenied exception is raised
    with pytest.raises(PermissionDenied, match='you are not an owner of this deduction!'):
        view.get_object(queryset=view.get_queryset())


@pytest.mark.django_db
def test_deduction_update_non_superuser_deduction(user, superuser):
    # Create a test Deduction object
    deduction = Deduction.objects.create(
        number_deduction='20250001',
        owner=superuser,
    )

    # Define the URL for the delete view
    url = reverse('apps.deduction:edit', kwargs={'pk': deduction.pk})

    # Create the request and attach a different user
    request = RequestFactory().put(url)
    request.user = user  # incorrect user

    # Create the view instance
    view = UpdateDeduction()
    view.request = request

    view.kwargs = {'pk': deduction.pk}

    # Verify that a PermissionDenied exception is raised
    with pytest.raises(PermissionDenied, match='you are not an owner of this deduction!'):
        view.post(request, pk=deduction.pk)


@pytest.mark.django_db
def test_deduction_update_superuser_deduction(user, superuser):
    # Create a test Deduction object
    deduction = Deduction.objects.create(
        number_deduction='20250001',
        owner=user,
    )

    # Define the URL for the delete view
    url = reverse('apps.deduction:edit', kwargs={'pk': deduction.pk})

    # Create the request and attach a different user
    request = RequestFactory().put(url)
    request.user = superuser  # incorrect user

    # Create the view instance
    view = UpdateDeduction()
    view.request = request
    view.kwargs = {'pk': deduction.pk}

    response = view.post(request, pk=deduction.pk)

    # Assert that the deduction object was deleted
    assert response.status_code == 200  # Redirection after successful deletion


@pytest.mark.django_db
def test_deduction_details(user, superuser):
    # Create a test Deduction object
    deduction = Deduction.objects.create(
        number_deduction='20250001',
        owner=user,
    )

    # Define the URL for the delete view
    url = reverse('apps.deduction:detail', kwargs={'pk': deduction.pk})

    # Create the request and attach a different user
    request = RequestFactory().put(url)
    request.user = superuser  # incorrect user

    # Create the view instance
    view = DeductionDetailView()
    view.request = request
    view.kwargs = {'pk': deduction.pk}

    response = view.get(request, pk=deduction.pk)

    # Assert that the deduction object was deleted
    assert response.status_code == 200  # Redirection after successful deletion


@pytest.mark.django_db
@patch('apps.deduction.mixins.Document')
@patch('apps.deduction.mixins.model_to_dict')
@patch('apps.deduction.mixins.finders.find')
@patch('apps.deduction.mixins.replace_placeholders_in_doc')
@patch('apps.deduction.mixins.set_font_size')
def test_generate_docx(
    mock_set_font_size,
    mock_replace_placeholders,
    mock_finders,
    mock_model_to_dict,
    mock_document,
):
    # Mock dependencies
    mock_facture_object = Mock()
    mock_model_to_dict.return_value = {'field1': 'value1'}
    mock_finders.return_value = '/mock/template/path'
    mock_doc = Mock()
    mock_document.return_value = mock_doc
    mock_file_stream = io.BytesIO()
    mock_doc.save = Mock()

    # Call the method
    view = BaseDeductionExportDocx()
    result = view.generate_docx(mock_facture_object, 'template.docx')

    # Assertions
    mock_model_to_dict.assert_called_once_with(mock_facture_object)
    mock_finders.assert_called_once_with('template.docx')
    mock_replace_placeholders.assert_called()
    mock_set_font_size.assert_called_once_with(mock_doc)
    assert isinstance(result, io.BytesIO)


@pytest.mark.django_db
@patch('apps.deduction.mixins.get_object_or_404')
@patch('apps.deduction.mixins.BaseDeductionExportDocx.generate_docx')
@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_generate_docx_get(
    mock_makedirs,
    mock_open_func,
    mock_generate_docx,
    mock_get_object_or_404,
):
    # Mock dependencies
    mock_deduction_object = Mock(number_deduction='123')
    mock_get_object_or_404.return_value = mock_deduction_object
    mock_file_stream = io.BytesIO(b'Test Content')
    mock_generate_docx.return_value = mock_file_stream

    # Mock request and kwargs
    mock_request = Mock()
    mock_kwargs = {'pk': 1}

    # Call the method
    view = BaseDeductionExportDocx()
    response = view.get(mock_request, **mock_kwargs)

    # Assertions
    mock_get_object_or_404.assert_called_once_with(Deduction, pk=1)
    mock_generate_docx.assert_called_once_with(mock_deduction_object, view.local_template)
    mock_open_func.assert_called_once_with(
        '/usr/src/app/apps/deduction/static/deduction/file_templates/file_output/deduction_123.docx',
        'wb',
    )
    mock_open_func().write.assert_called_once_with(b'Test Content')
    mock_makedirs.assert_called_once_with(
        '/usr/src/app/apps/deduction/static/deduction/file_templates/file_output',
        exist_ok=True,
    )
    assert response['Content-Disposition'] == 'attachment; filename="deduction_123.docx"'
    assert (
        response['Content-Type']
        == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    assert response.content == b'Test Content'
