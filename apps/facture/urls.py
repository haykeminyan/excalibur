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
    WorldFactureListView,
)

app_name = 'apps.facture'
urlpatterns = [
    # Facture creation
    path('local/create/', AddLocalFacture.as_view(), name='local_create'),
    path('world/create/', AddWorldFacture.as_view(), name='world_create'),
    path(
        'local/update/<int:pk>/',
        UpdateLocalFacture.as_view(),
        name='local_update',
    ),
    path(
        'world/update/<int:pk>/',
        UpdateWorldFacture.as_view(),
        name='world_update',
    ),
    path(
        'local/delete/<int:pk>/',
        DeleteLocalFacture.as_view(),
        name='local_delete',
    ),
    path(
        'world/delete/<int:pk>/',
        DeleteWorldFacture.as_view(),
        name='world_delete',
    ),
    # Facture listing
    path('local/', LocalFactureListView.as_view(), name='local_list'),
    path('world/', WorldFactureListView.as_view(), name='world_list'),
    # Facture details
    path('local/<int:pk>/', LocalFactureDetailView.as_view(), name='local_detail'),
    path('world/<int:pk>/', WorldFactureDetailView.as_view(), name='world_detail'),
    path(
        'local/generate-docx/<int:pk>/',
        BaseFactureLocalExportDocx.as_view(),
        name='generate-local-docx',
    ),
    path(
        'world/generate-docx/<int:pk>/',
        BaseFactureWorldExportDocx.as_view(),
        name='generate-world-docx',
    ),
]
