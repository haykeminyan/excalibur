from django.urls import path

from apps.main.views import MainMenuListView

app_name = 'apps.main'

urlpatterns = [
    path('', MainMenuListView.as_view(), name='main_menu'),
]
