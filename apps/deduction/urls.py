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

from apps.deduction import views
from apps.deduction.mixins import BaseDeductionExportDocx, download_deduction_document
from apps.deduction.tasks import task_status

app_name = 'apps.deduction'
urlpatterns = [
    path('', views.DeductionListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.DeductionDetailView.as_view(), name='detail'),
    path('create/', views.AddDeduction.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateDeduction.as_view(), name='edit'),
    path('delete/<int:pk>/', views.DeleteDeduction.as_view(), name='delete'),
    path(
        'generate-docx/<int:pk>/',
        BaseDeductionExportDocx.as_view(),
        name='generate-deduction-docx',
    ),
    # path('generated_documents/<str:file_name>/', download_deduction_document, name='download_deduction_document'),
    path('<int:pk>/export/', BaseDeductionExportDocx.as_view(), name='export_deduction_document'),
    path('task_status/<str:task_id>/', task_status, name='task_status'),
    path('generated_documents/<str:file_name>/', download_deduction_document,
         name='download_deduction_document'),
]
