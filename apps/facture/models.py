import logging

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class Facture(models.Model):
    number_facture = models.CharField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    firm_name = models.CharField(max_length=255)
    created_date = models.DateField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    reference = models.CharField(default='', max_length=10, blank=True, null=True)
    quantity = models.IntegerField()
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity_after_percent = models.FloatField()
    total_tax = models.FloatField()
    net_pay = models.FloatField()


class LocalFacture(Facture):
    # check if this fucking shit has reason to exist
    destination = models.CharField(max_length=255, default='Recharge express')
    deposit = models.FloatField(blank=True, null=True)
    tax_ht = models.FloatField()
    total_ttc = models.FloatField()
    total_sum_fr = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Ensure the owner is set when saving a LocalFacture instance
        if not self.owner:
            self.owner = self.user  # or self.request.user if accessible
        super().save(*args, **kwargs)


class WorldFacture(Facture):
    account_number = models.IntegerField()
    receiver = models.CharField(max_length=200, blank=True, null=True)
    sku = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, default='Recharge Card and Express')
    specification = models.IntegerField(blank=True, null=True)
    shipping_fee = models.FloatField(blank=True, null=True)
    total_sum_en = models.CharField(max_length=255)
