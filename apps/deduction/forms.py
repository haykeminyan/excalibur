import logging
from datetime import date
from django import forms

from apps.deduction.models import Deduction

logger = logging.getLogger(__name__)


def get_next_deduction_number():
	"""Helper function to calculate the next available facture number"""
	last_local_facture = Deduction.objects.all().order_by('number_deduction').last()

	local_number = int(last_local_facture.number_deduction) if last_local_facture else 0

	return local_number + 1 if local_number else int(f'{date.today().year}0001')


class DeductionFormBase(forms.ModelForm):
	"""Base form to handle facture number logic"""

	def __init__(self, *args, **kwargs):
		super(DeductionFormBase, self).__init__(*args, **kwargs)

		# Automatically generate and prefill the 'number_facture'
		next_facture_number = get_next_deduction_number()
		self.fields['number_deduction'].initial = str(next_facture_number)
		self.fields['number_deduction'].widget.attrs['readonly'] = True
		self.fields['number_deduction'].disabled = True


class DeductionForm(DeductionFormBase):
	"""Form for creating LocalFacture"""

	class Meta:
		model = Deduction
		fields = '__all__'
		widgets = {
			'owner': forms.HiddenInput(),
			'created_date': forms.DateInput(attrs={'type': 'date'}),
			'date_regulations': forms.DateInput(attrs={'type': 'date'})
		}

	def __init__(self, *args, **kwargs):
		super(DeductionForm, self).__init__(*args, **kwargs)
		self.fields['number_deduction'].label = 'Numero'

