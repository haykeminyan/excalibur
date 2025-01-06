import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


@csrf_exempt
def healthcheck(request):
    db_health = 'healthy'
    try:
        connections['default'].cursor()
    except OperationalError:
        db_health = 'unhealthy'
    return JsonResponse({'status': 'healthy', 'database': db_health})


# Create your views here.
class MainMenuListView(TemplateView, LoginRequiredMixin):
    template_name = 'html/main_menu.html'
