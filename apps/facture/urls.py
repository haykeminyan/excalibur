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
from apps.facture.models import Facture, WorldFacture
from apps.facture.views import LocalFactureListView, WorldFactureListView, LocalFactureDetailView, \
    WorldFactureDetailView, AddLocalFacture, AddWorldFacture

urlpatterns = [
    # Facture creation
    path('facture/local/create/', AddLocalFacture.as_view(), name='facture_local_create'),
    path('facture/world/create/', AddWorldFacture.as_view(), name='facture_world_create'),

    # Facture listing
    path('facture/local/', LocalFactureListView.as_view(), name='facture_local_list'),
    path('facture/world/', WorldFactureListView.as_view(), name='facture_world_list'),

    # Facture details
    path('facture/local/<int:pk>/', LocalFactureDetailView.as_view(), name='facture_local_detail'),
    path('facture/world/<int:pk>/', WorldFactureDetailView.as_view(), name='facture_world_detail'),
]