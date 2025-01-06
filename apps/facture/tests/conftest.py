import logging

import pytest
from django.contrib.auth.models import User
from django.db import connection
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


@pytest.fixture(autouse=True)
def truncate_all_tables(db):
    """
    Truncate all tables in the database before each test to ensure a clean state.
    """
    # Get a list of all tables in the database
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public'",
        )
        tables = cursor.fetchall()

    # Truncate all tables
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table[0]} RESTART IDENTITY CASCADE;")
            print(f"Truncated table: {table[0]}")
