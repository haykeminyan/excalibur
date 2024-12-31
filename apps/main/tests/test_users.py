import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def factory():
    return RequestFactory()
