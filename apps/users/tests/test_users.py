import importlib
import logging
from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse

import excalibur.settings as settings
from apps.users.tests.constants import (
    url_names_from_deduction,
    url_names_from_facture,
    url_names_from_fail,
    url_names_from_main,
    url_names_from_users,
    url_to_view_mapping,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test__all_main_apps_redirect_to_login(factory):
    # Combine all URL names from different sources
    all_url_names = [
        *url_names_from_deduction,
        *url_names_from_facture,
        *url_names_from_fail,
    ]

    # Test each URL
    for url_name in all_url_names:
        if any(
            keyword in url_name for keyword in ['detail', 'edit', 'update', 'delete', 'generate']
        ):
            # Assuming you know the pk (e.g., pk=1)
            request = factory.get(reverse(url_name, kwargs={'pk': 1}))
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
def test__main_app(factory):
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
def test__user_app_fail(factory):
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
def test__user_success_login(client, user):
    # Simulate a POST request with valid credentials
    response = client.post(
        reverse('apps.users:login'),
        {
            'username': user.username,
            'password': 'password',
        },
    )

    # Assert redirection to the success_url
    assert response.status_code == 302
    assert response.url == '/main/'


@pytest.mark.parametrize('environment', ['production', 'development'])
def test__enviroment_settings(monkeypatch, environment):
    monkeypatch.setenv('ENVIRONMENT', environment)
    importlib.reload(settings)  # Reimport and execute settings.py

    if environment == 'production':
        assert settings.SECURE_SSL_REDIRECT is True
        assert settings.SECURE_PROXY_SSL_HEADER == ('HTTP_X_FORWARDED_PROTO', 'https')

    elif environment == 'development':
        assert settings.SECURE_SSL_REDIRECT is False
        assert settings.SECURE_PROXY_SSL_HEADER is None
