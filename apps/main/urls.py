from django.urls import path

from apps.main.views import MainMenuListView, healthcheck

app_name = 'apps.main'

urlpatterns = [
    path('healthcheck/', healthcheck, name='healthcheck'),
    path('', MainMenuListView.as_view(), name='main_menu'),
]
