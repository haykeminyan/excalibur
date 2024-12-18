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

from django.urls import path

from apps.facture.mixins import BaseFactureLocalExportDocx, BaseFactureWorldExportDocx
from apps.facture.views import (
    AddLocalFacture,
    AddWorldFacture,
    DeleteLocalFacture,
    DeleteWorldFacture,
    LocalFactureDetailView,
    LocalFactureListView,
    UpdateLocalFacture,
    UpdateWorldFacture,
    WorldFactureDetailView,
    WorldFactureListView
)

urlpatterns = [
    # Facture creation
    path('facture/local/create/', AddLocalFacture.as_view(), name='facture_local_create'),
    path('facture/world/create/', AddWorldFacture.as_view(), name='facture_world_create'),
    path(
        'facture/local/update/<int:pk>/',
        UpdateLocalFacture.as_view(),
        name='facture_local_update',
    ),
    path(
        'facture/world/update/<int:pk>/',
        UpdateWorldFacture.as_view(),
        name='facture_world_update',
    ),
    path(
        'facture/local/delete/<int:pk>/',
        DeleteLocalFacture.as_view(),
        name='facture_local_delete',
    ),
    path(
        'facture/world/delete/<int:pk>/',
        DeleteWorldFacture.as_view(),
        name='facture_world_update',
    ),
    # Facture listing
    path('facture/local/', LocalFactureListView.as_view(), name='facture_local_list'),
    path('facture/world/', WorldFactureListView.as_view(), name='facture_world_list'),
    # Facture details
    path('facture/local/<int:pk>/', LocalFactureDetailView.as_view(), name='facture_local_detail'),
    path('facture/world/<int:pk>/', WorldFactureDetailView.as_view(), name='facture_world_detail'),
    path(
        'facture/local/generate-docx/<int:pk>/',
        BaseFactureLocalExportDocx.as_view(),
        name='generate-local-docx',
    ),
    path(
        'facture/world/generate-docx/<int:pk>/',
        BaseFactureWorldExportDocx.as_view(),
        name='generate-world-docx',
    ),
]
