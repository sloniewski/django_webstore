from django.shortcuts import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
)

from webstore.product.models import Product

class DashboardWelcomeView(TemplateView):
    """
    Generic TemplateView,
    **Template:**
    :template:`dasboard/base_dashboard.html`
    """
    template_name = 'dashboard/base_dashboard.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'dashboard/product/product_create.html'
    fields = [
        'name',
        'slug',
        'description',
        'weight',
    ]

    def get_success_url(self):
        return reverse('dashboard:product-list')


class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/product/product_list.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'dashboard/product/product_update.html'
    fields = [
        'name',
        'slug',
        'description',
        'weight',
    ]


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'dashboard/product/product_delete.html'
