from django.contrib import admin

# Register your models here.
from .models import LocalFacture, WorldFacture

admin.site.register(LocalFacture)
admin.site.register(WorldFacture)
