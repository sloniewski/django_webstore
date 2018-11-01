from webstore.product.models import Product

from django.views import generic


class ProductListView(generic.ListView):
    model = Product
    template_name = 'dashboard/product/product_list.html'
