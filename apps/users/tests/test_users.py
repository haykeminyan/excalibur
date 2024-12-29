from unittest.mock import patch

import pytest
from django.middleware.csrf import get_token
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from apps.deduction.views import DeductionListView
from apps.facture.views import LocalFactureListView
import logging

from apps.main.views import MainMenuListView
from apps.users.tests.constants import url_names_from_deduction, url_names_from_facture, url_names_from_users, \
    url_names_from_main, url_to_view_mapping, url_names_from_fail

logger = logging.getLogger(__name__)

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test_all_main_apps_redirect_to_login(factory):
    # Combine all URL names from different sources
    all_url_names = [
        *url_names_from_deduction,
        *url_names_from_facture,
        *url_names_from_fail,
    ]

    # Test each URL
    for url_name in all_url_names:
        if any(keyword in url_name for keyword in ['detail', 'edit', 'update', 'delete', 'generate']):
            # Assuming you know the pk (e.g., pk=1)
            request = factory.get(reverse(url_name, kwargs={'pk':1}))
        elif url_name in url_names_from_fail:
            with patch('pytest.fail') as mock_fail:
                mock_fail(url_name)
        else:
            request = factory.get(reverse(url_name))  # No pk needed for other URLs
        request.user = AnonymousUser()  # Simulate an anonymous user

        # Dynamically get the view associated with the URL name
        view = url_to_view_mapping.get(url_name)
        if view:
            response = view.as_view()(request)  # Call the view
            assert response.status_code == 302  # Ensure it's a redirect
            assert '/users/login/' in response.url  # Ensure redirect is to login


@pytest.mark.django_db
def test_main_app(factory):
    # Combine all URL names from different sources
    all_url_names = [
        *url_names_from_main,
        *url_names_from_fail,
    ]

    # Test each URL
    for url_name in all_url_names:
        if url_name in url_names_from_fail:
            with patch('pytest.fail') as mock_fail:
                mock_fail(url_name)
        else:
            request = factory.get(reverse(url_name))
            request.user = AnonymousUser()  # Simulate an anonymous user

            # Dynamically get the view associated with the URL name
            view = url_to_view_mapping.get(url_name)
            if view:
                response = view.as_view()(request)
                assert response.status_code == 200

@pytest.mark.django_db
def test_user_app_fail(factory):
    # Combine all URL names from different sources
    all_url_names = [
        *url_names_from_users,
        *url_names_from_fail,
    ]

    # Test each URL
    for url_name in all_url_names:
        if url_name in url_names_from_fail:
            with patch('pytest.fail') as mock_fail:
                mock_fail(url_name)
        else:
            request = factory.post(reverse(url_name))
            request.user = AnonymousUser()  # Simulate an anonymous user

            # Dynamically get the view associated with the URL name
            view = url_to_view_mapping.get(url_name)
            if view:
                response = view.as_view()(request)
                assert response.status_code == 403
                assert 'CSRF verification failed' in str(response.content)

@pytest.mark.django_db
def test_user_app_succeed(client, user):
    all_url_names = [
        *url_names_from_users
    ]

    for url_name in all_url_names:
        client.force_login(user)  # Simulate a logged-in user
        response = client.post(reverse(url_name))
        # If the response is a redirect (status code 302), check the 'Location' header
        if response.status_code == 302:
            print(f"Redirecting to: {response['Location']}")
            assert '/users/login/' in response['Location']
        else:
            # If it's not a redirect, access the _request attribute to get the path
            print(f"Response URL path: {response._request.path_info}")
            assert response.status_code == 200


@pytest.mark.django_db
def test_login_success(factory, user):
    request = factory.get(reverse('apps.facture:local_list'))
    request.user = user
    response = LocalFactureListView.as_view()(request)
    assert response.status_code == 200