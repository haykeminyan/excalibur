from django.http import JsonResponse
from django.shortcuts import render
from apps.facture.forms import LocalFactureForm, WorldFactureForm


def render_form_response(request, facture_form, facture_type):
    template_mapping = {
        'local': 'html/create-facture-local.html',
        'world': 'html/create-facture-world.html'
    }

    template_name = template_mapping.get(facture_type)
    if template_name:
        return render(request, template_name, {'facture_form': facture_form})

    return JsonResponse({'error': 'Invalid facture type'}, status=400)


def get_facture_form(facture_type, data):
    form_mapping = {
        'local': LocalFactureForm,
        'world': WorldFactureForm
    }

    form_class = form_mapping.get(facture_type)
    if form_class:
        return form_class(data=data)

    raise ValueError(f"Invalid facture type: {facture_type}")


def handle_facture_form(form):
    if form.is_valid():
        instance = form.save()
        return JsonResponse({
            'success': 'Facture created successfully.',
            'id': instance.id  # Optionally return the ID or other details
        }, status=201)

    # Construct a detailed error response with the form errors
    error_response = {
        'errors': form.errors,
        'message': 'Failed to create facture due to validation errors.'
    }
    return JsonResponse(error_response, status=400)