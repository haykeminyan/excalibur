from django import forms

from apps.facture.models import Facture, WorldFacture, LocalFacture
import logging

logger = logging.getLogger(__name__)

class LocalFactureForm(forms.ModelForm):
    class Meta:
        model = LocalFacture
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # Explicitly specify date input type
        }
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(LocalFactureForm, self).__init__(*args, **kwargs)
        self.fields['number_facture'].label = 'Numero'
        self.fields['quantity'].label = 'Quantityé'
        self.fields['percent'].label = 'P.U.TTC'
        self.fields['total_tax'].label = 'Total H.T.'

class WorldFactureForm(forms.ModelForm):
    class Meta:
        model = WorldFacture
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WorldFactureForm, self).__init__(*args, **kwargs)
        self.fields['number_facture'].label = 'Numero'
        self.fields['quantity'].label = 'Quantityé'
        self.fields['percent'].label = 'P.U.TTC'
        self.fields['total_tax'].label = 'Total H.T.'