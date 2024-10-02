from django import forms

from apps.facture.models import Facture


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        self.fields['number_facture'].label = 'Numero'
        self.fields['quantity'].label = 'Quantityé'
        self.fields['percent'].label = 'P.U.TTC'
        self.fields['total_tax'].label = 'Total H.T.'
        print(self.fields)
