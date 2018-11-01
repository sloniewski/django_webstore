from django.views.generic import DetailView
from django.core.paginator import Paginator

from django_filters.views import FilterView

from .models import Product
from .forms import FilterProductsForm


class ProductDetailView(DetailView):
    model = Product


class ProductListView(FilterView):
    template_name = 'product/product_list.html'
    filterset_class = FilterProductsForm
    strict = False
    queryset = Product.objects.with_prices()
