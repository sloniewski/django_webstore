from django.http import JsonResponse

class AjaxResponseMixin:

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
        raise NotImplementedError('You need to provide this method')

class ForceSessionMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)