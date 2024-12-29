
import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User

from apps.facture.views import LocalFactureListView


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def factory():
    return RequestFactory()
