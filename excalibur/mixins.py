import json
from django.http import HttpResponseBadRequest
from django.views import View

class JsonRequestMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.content_type == "application/json":
            try:
                request.data = json.loads(request.body)
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Invalid JSON")
        else:
            request.data = request.POST
        return super().dispatch(request, *args, **kwargs)


