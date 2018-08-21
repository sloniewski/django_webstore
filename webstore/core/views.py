from django.views.generic import ListView


class FilterView(ListView):
    model = None
    template_name = None
    filter_form_class = None
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.request.GET._mutable = True
        try:
            self.request.GET.pop('page')
        except KeyError:
            pass
        context.update({
            'filter_form': self.filter_form_class(self.request.GET),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_form = self.filter_form_class(self.request.GET)
        if filter_form.is_valid():
            filters = filter_form.get_filters()
            if filters != []:
                queryset = queryset.filter(*filters)
        return queryset
