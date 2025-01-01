from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'html/login.html'
    success_url = 'apps.facture:local_list'


class LogoutUser(LogoutView):
    template_name = 'html/login.html'

    def dispatch(self, request, *args, **kwargs):
        # Remove the language cookie on logout
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie('django_language')  # Remove the language cookie
        return response
