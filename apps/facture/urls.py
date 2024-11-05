"""
URL configuration for excalibur project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps import facture
from apps.facture.models import Facture
from apps.facture.views import FactureCreateView, LocalFactureListView, WorldFactureListView

urlpatterns = [
    path('create-facture', FactureCreateView.as_view(), name='create-facture'),
    path('local-list-facture', LocalFactureListView.as_view(), name='local-list-facture'),
    path('world-list-facture', WorldFactureListView.as_view(), name='world-list-facture'),
]
