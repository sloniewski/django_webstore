from django.views.generic import DetailView
from django.core.paginator import Paginator

from django_filters.views import FilterView

from .models import Product
from .forms import FilterProductsForm


class ProductDetailView(DetailView):
    model = Product
    template_name = 'webstore/product/product_detail.html'


class ProductListView(FilterView):
    template_name = 'webstore/product/product_list.html'
    filterset_class = FilterProductsForm
    strict = False
    queryset = Product.objects.with_prices().filter(price__isnull=False)
