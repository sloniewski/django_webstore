from django.views.generic import DetailView
from django.core.paginator import Paginator

from webstore.core.views import FilterView
from .models import Product
from .forms import FilterProductsForm


class ProductDetailView(DetailView):
    model = Product


class ProductListView(FilterView):
    model = Product
    template_name = 'product/product_list.html'
    filter_form_class = FilterProductsForm
    queryset = Product.objects.with_prices()
