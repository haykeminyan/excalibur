from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import date

class Deductions(models.Model):
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
	montant_ttc = models.FloatField(blank=True, null=True)
	montant_ht = models.FloatField(blank=True, null=True)
	taux_tva = models.CharField(default='', max_length=20, blank=True, null=True)
	montant_tva = models.FloatField(blank=True, null=True)
	prorated_rate = models.CharField(default='', max_length=20, blank=True, null=True)
	date_regulations = models.DateField(default=timezone.now)
	payment_choice = models.CharField(max_length=250, blank=True, null=True)
	cr = models.CharField(default='', max_length=20, blank=True, null=True)
	ice = models.TextField(blank=True, null=True)

	def __str__(self) -> str:
		"""Return model string representation."""
		owner = self.owner if self.owner else "Unknown Owner"
		supplier = self.supplier if self.supplier else "Unknown Supplier"
		return f'{owner} {supplier}'

	def save(self, *args, **kwargs):
		if not self.pk:  # Object is being created
			year = date.today().year
			last_deduction = Deductions.objects.filter(
				created_date__year=year
			).order_by('id').last()

			# Determine the last number and generate the new one
			if last_deduction:
				# Extract the numeric part of the last number_deduction
				last_number = int(last_deduction.number_deduction[-4:])
				new_number = last_number + 1
			else:
				new_number = 1

			# Format the new number as 'YYYYxxxx'
			self.number_deduction = f'{year}{new_number:04d}'

		super().save(*args, **kwargs)
