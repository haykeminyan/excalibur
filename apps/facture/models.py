from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


class Facture(models.Model):
    address = models.TextField()
    number_facture = models.IntegerField(default=date.today().year)
    owner = models.ForeignKey(
        'auth.User',
        related_name='factures',
        on_delete=models.CASCADE,
        null=True,
    )
    date = models.DateField(default=date.today())
    update_time = models.DateTimeField(auto_now=True)
    reference = models.CharField(default='', max_length=10, blank=True, null=True)
    quantity = models.IntegerField()
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity_after_percent = models.FloatField()
    total_tax = models.FloatField()
    total_payment_after_tax = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Use pk to check if instance is new
            super().save(*args, **kwargs)  # Save the instance first
            # Update number_facture with formatted id
            if self.pk:
                self.number_facture = int(f"{self.number_facture:04d}{self.pk:04d}")
                self.save(update_fields=['number_facture'])  # Save updated number_facture
        super().save(*args, **kwargs)  # Ensure final save

class LocalFacture(Facture):
    # check if this fucking shit has reason to exist
    identification_number = models.IntegerField(blank=True, null=True)
    destination = models.CharField(max_length=255, default='Recharge express')
    deposit = models.FloatField(blank=True, null=True)


    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.date} {self.id}'


class WorldFacture(Facture):
    firm_name = models.TextField()
    account_number = models.IntegerField()
    sku = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    specification = models.IntegerField(blank=True, null=True)


    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.date} {self.id}'
