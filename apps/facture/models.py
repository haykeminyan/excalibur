import logging
from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

logger = logging.getLogger(__name__)


class Facture(models.Model):
    number_facture = models.CharField(default=date.today().year, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    firm_name = models.CharField(max_length=255)
    date = models.DateField(default=date.today())
    update_time = models.DateTimeField(auto_now=True)
    reference = models.CharField(default='', max_length=10, blank=True, null=True)
    quantity = models.IntegerField()
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity_after_percent = models.FloatField()
    total_tax = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.pk:
            last_local_facture = LocalFacture.objects.all().order_by('number_facture').last()
            last_world_facture = WorldFacture.objects.all().order_by('number_facture').last()

            local_number = int(last_local_facture.number_facture) if last_local_facture else 0
            world_number = int(last_world_facture.number_facture) if last_world_facture else 0

            if local_number or world_number:
                last_number_facture = max(local_number, world_number) + 1
            else:
                last_number_facture = int(f'{date.today().year}0001')
            self.number_facture = str(last_number_facture)

        super().save(*args, **kwargs)


class LocalFacture(Facture):
    # check if this fucking shit has reason to exist
    destination = models.CharField(max_length=255, default='Recharge express')
    deposit = models.FloatField(blank=True, null=True)
    tax_ht = models.FloatField()
    total_ttc = models.FloatField()
    net_pay = models.FloatField()
    total_sum_fr = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.date} {self.id}'

    def save(self, *args, **kwargs):
        # Ensure the owner is set when saving a LocalFacture instance
        if not self.owner:
            self.owner = self.user  # or self.request.user if accessible
        super().save(*args, **kwargs)


class WorldFacture(Facture):
    account_number = models.IntegerField()
    sku = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    specification = models.IntegerField(blank=True, null=True)
    total_sum_en = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.date} {self.id}'
