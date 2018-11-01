from django.shortcuts import reverse, get_object_or_404

from webstore.product.models import Product, Price

from django_filters.views import FilterView
from django.views import generic

from .forms import ProductFilterForm


class ProductListView(FilterView):
    model = Product
    template_name = 'dashboard/product/product_list.html'
    strict = False
    filterset_class = ProductFilterForm


class ProductCreateView(generic.CreateView):
    template_name = 'dashboard/product/product_create.html'
    model = Product
    fields = '__all__'

    def get_success_url(self):
        return reverse('dashboard:product-list')


class ProductUpdateView(generic.UpdateView):
    model = Product
    template_name = 'dashboard/product/product_update.html'
    fields = [
        'name',
        'active',
        'slug',
        'description',
        'weight',
    ]


class ProductDeleteView(generic.DeleteView):
    model = Product
    template_name = 'dashboard/product/product_delete.html'


class ProductPriceListView(generic.ListView):
    model = Price
    template_name = 'dashboard/product/product_price_list.html'

    def get_queryset(self):
        number = self.request.resolver_match.kwargs['number']
        product = get_object_or_404(Product, number=number)
        self.update_context({'product': product})
        return Price.objects.filter(product=product)

    def update_context(self, data_dict):
        if self.extra_context is None:
            self.extra_context = data_dict
        else:
            self.extra_context.update(data_dict)
