import logging

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory

logger = logging.getLogger(__name__)


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(username='superuser', password='password')


@pytest.fixture
def factory():
    return RequestFactory()
