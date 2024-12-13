import logging

from django import template

logger = logging.getLogger(__name__)


register = template.Library()


@register.filter
def get_current_filter_value(request, *args):
    """
    Returns the value of the currently selected filter option.
    """
    if not hasattr(request, 'GET'):
        return ''
    selected_filter = request.GET.get('filter_option')
    return request.GET.get(selected_filter, '')
