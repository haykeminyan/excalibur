from django.views import View
from django.shortcuts import render, redirect
from .forms import FactureForm  # Ensure you have this form imported

class FactureCreateView(View):
    def get(self, request):
        facture_form = FactureForm()  # Initialize an empty form
        return render(request, 'html/create-facture.html', {'facture_form': facture_form})

    def post(self, request):
        facture_form = FactureForm(request.POST)
        if facture_form.is_valid():
            facture_form.save()  # Save the form to the database
            return redirect('create-facture-success')  # Redirect to a success page or another view
        else:
            # Print form errors for debugging
            print(facture_form.errors)
        return render(request, 'html/create-facture.html', {'facture_form': facture_form})
