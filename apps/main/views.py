from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db.utils import OperationalError

@csrf_exempt
def healthcheck(request):
    db_health = "healthy"
    try:
        connections['default'].cursor()
    except OperationalError:
        db_health = "unhealthy"
    return JsonResponse({"status": "healthy", "database": db_health})



# Create your views here.
class MainMenuListView(TemplateView, LoginRequiredMixin):
    template_name = 'html/main_menu.html'