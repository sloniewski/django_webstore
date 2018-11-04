from django.views import View
from django.http import JsonResponse

class AjaxResponseMixin(View):
    http_method_names = ['post', 'head', 'options', 'trace']

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(self.get_response_data())
        else:
            return response

    def get_response_data(self):

