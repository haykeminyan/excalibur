import logging

import pytest
from django.http import QueryDict

from apps.facture.templatetags.custom_filters import get_current_filter_value

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.parametrize('filter_value', ['foo', 'boo'])
def test__custom_filter(monkeypatch, request, filter_value):
    request.GET = QueryDict(f'filter_option=test&test={filter_value}')
    filter = get_current_filter_value(request)
    assert filter == filter_value


@pytest.mark.django_db
def test__custom_filter_empty(monkeypatch, request):
    filter = get_current_filter_value(request)
    assert filter == ''
