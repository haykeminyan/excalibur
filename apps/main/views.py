from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.
class MainMenuListView(TemplateView, LoginRequiredMixin):
    template_name = 'html/main_menu.html'