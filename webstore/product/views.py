from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator

from .models import Product
from .forms import FilterProductsForm


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    form_class = FilterProductsForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({'form': self.form_class()})
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid:
            filters = form.get_filters()
            if filters != []:
                return self.model.objects.filter(*filters)

        return Product.objects.all()
