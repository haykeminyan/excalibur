from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'html/login.html'
    extra_context = {'title': 'Authorization'}

    def get_success_url(self):
        return reverse_lazy('local_list')


class LogoutUser(LogoutView):
    template_name = 'html/login.html'
