from unittest.mock import patch

import pytest
from django.db import OperationalError
from django.urls import reverse_lazy


@pytest.mark.django_db
def test_healthcheck(client):
    # given
    with patch('apps.main.views.connections') as mock_connections:
        # Simulate a database connection failure
        mock_connections.__getitem__.return_value.cursor.side_effect = OperationalError

        # when
        response = client.get(reverse_lazy('apps.main:healthcheck'))

        # then
        assert response.status_code in [200, 301]