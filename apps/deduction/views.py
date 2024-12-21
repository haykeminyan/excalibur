# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class DeductionList(View):
    template_name = 'html/main_menu.html'