from datetime import datetime

from django.db import models


class Deductions(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.today)
    number_facture = models.CharField(max_length=50)
    owner = models.ForeignKey(
        'auth.User',
        related_name='deductions',
        on_delete=models.CASCADE,
        null=True,
    )
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
    code_tva = models.CharField(default='', max_length=20, blank=True, null=True)
    montant_tva = models.FloatField(blank=True, null=True)
    prorated_rate = models.CharField(default='', max_length=20, blank=True, null=True)
    date_regulations = models.DateField(default=datetime.today)
    payment_choice = models.CharField(max_length=250, blank=True, null=True)
    cr = models.CharField(default='', max_length=20, blank=True, null=True)
    ice = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        """Return model string representation."""
        return f'{self.owner} {self.supplier}'
