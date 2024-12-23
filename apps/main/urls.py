from django.urls import path

from apps.main.views import MainMenuListView, healthcheck, robots_txt

app_name = 'apps.main'

urlpatterns = [
    path('healthcheck/', healthcheck),
    path("robots.txt", robots_txt),
    path('', MainMenuListView.as_view(), name='main_menu'),
]
