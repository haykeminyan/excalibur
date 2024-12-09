from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from apps.users.forms import LoginUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'html/login.html'
    extra_context = {'title': "Authorization"}

    def get_success_url(self):
        return reverse_lazy('facture_local_list')


class LogoutUser(LogoutView):
    template_name = 'html/login.html'