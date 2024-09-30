from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


class Facture(models.Model):
    id = models.AutoField(primary_key=True)
    number_facture = models.IntegerField(default=date.today().year)
    owner = models.ForeignKey(
        'auth.User',
        related_name='factures',
        on_delete=models.CASCADE,
        null=True,
    )
    firm_name = models.CharField(max_length=255)
    address = models.TextField()
    date = models.DateField(default=date.today)
    facture_type = models.CharField(
        choices=[('internal', 'Internal'), ('world', 'World')],
        max_length=10
    )
    update_time = models.DateField(auto_now=True)
    reference = models.CharField(default='', max_length=10, blank=True)
    destination = models.CharField(default='Recharge Express', max_length=30)
    quantity = models.IntegerField(blank=True, null=True)
    percent = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity_after_percent = models.FloatField(blank=True, null=True)
    advance_payment = models.CharField(default='', max_length=10, blank=True)
    total_tax = models.FloatField(blank=True, null=True)
    total_payment_after_tax = models.FloatField(blank=True, null=True)
    total_sum_fr = models.TextField()
    total_sum_en = models.TextField()
    contract_date = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Use pk to check if instance is new
            super().save(*args, **kwargs)  # Save the instance first
            # Update number_facture with formatted id
            if self.pk:
                self.number_facture = int(f"{self.number_facture:04d}{self.pk:04d}")
                self.save(update_fields=['number_facture'])  # Save updated number_facture
        super().save(*args, **kwargs)  # Ensure final save

    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.date} {self.id}'
