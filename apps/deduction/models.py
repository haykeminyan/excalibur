from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Deduction(models.Model):
	created_date = models.DateField(default=timezone.now)
	number_deduction = models.CharField(max_length=20, unique=True, blank=True, null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	ifn = models.CharField(default='', max_length=20, blank=True, null=True)
	supplier = models.CharField(max_length=200)
	nature_of_products = models.CharField(
		max_length=150,
		blank=True,
		null=True,
		default='ACHAT PRESTATIONS DE SERV',
	)
	update_time = models.DateTimeField(auto_now=True)
	montant_ttc = models.FloatField(blank=True, null=True)
	montant_ht = models.FloatField(blank=True, null=True)
	taux_tva = models.CharField(default='', max_length=20, blank=True, null=True)
	montant_tva = models.FloatField(blank=True, null=True)
	proporated_rate = models.CharField(default='', max_length=20, blank=True, null=True)
	date_regulations = models.DateField(default=timezone.now)
	payment_choice = models.CharField(max_length=250, blank=True, null=True)
	cr = models.CharField(default='', max_length=20, blank=True, null=True)
	ice = models.CharField(default='', max_length=20, blank=True, null=True)
