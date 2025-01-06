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
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.i18n import set_language

from apps.deduction.views import trigger_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('', lambda request: redirect('/main/')),  # This will redirect to /main
    path('facture/', include('apps.facture.urls', namespace='facture')),
    path('deduction/', include('apps.deduction.urls', namespace='deduction')),
    path('main/', include('apps.main.urls', namespace='main')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set_language/', set_language, name='set_language'),
    path('sentry-debug/', trigger_error),
]
