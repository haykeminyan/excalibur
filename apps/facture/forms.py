import logging
from datetime import date
from django import forms
from apps.facture.models import LocalFacture, WorldFacture

logger = logging.getLogger(__name__)


def get_next_facture_number():
	"""Helper function to calculate the next available facture number"""
	last_local_facture = LocalFacture.objects.all().order_by('number_facture').last()
	last_world_facture = WorldFacture.objects.all().order_by('number_facture').last()

	local_number = int(last_local_facture.number_facture) if last_local_facture else 0
	world_number = int(last_world_facture.number_facture) if last_world_facture else 0

	return max(local_number, world_number) + 1 if local_number or world_number else int(f'{date.today().year}0001')


class FactureFormBase(forms.ModelForm):
	"""Base form to handle facture number logic"""

	def __init__(self, *args, **kwargs):
		super(FactureFormBase, self).__init__(*args, **kwargs)

		# Automatically generate and prefill the 'number_facture'
		next_facture_number = get_next_facture_number()
		self.fields['number_facture'].initial = str(next_facture_number)
		self.fields['number_facture'].widget.attrs['readonly'] = True
		self.fields['number_facture'].disabled = True


class LocalFactureForm(FactureFormBase):
	"""Form for creating LocalFacture"""

	class Meta:
		model = LocalFacture
		fields = '__all__'
		widgets = {
			'owner': forms.HiddenInput(),
			'created_date': forms.DateInput(attrs={'type': 'date'}),
		}

	def __init__(self, *args, **kwargs):
		super(LocalFactureForm, self).__init__(*args, **kwargs)
		self.fields['number_facture'].label = 'Numero'
		self.fields['quantity'].label = 'Quantité'
		self.fields['percent'].label = 'P.U.TTC'
		self.fields['total_tax'].label = 'Total H.T.'


class WorldFactureForm(FactureFormBase):
	"""Form for creating WorldFacture"""

	class Meta:
		model = WorldFacture
		fields = '__all__'
		widgets = {
			'owner': forms.HiddenInput(),
			'created_date': forms.DateInput(attrs={'type': 'date'}),
		}

	def __init__(self, *args, **kwargs):
		super(WorldFactureForm, self).__init__(*args, **kwargs)
		self.fields['receiver'].label = 'Bill to'
