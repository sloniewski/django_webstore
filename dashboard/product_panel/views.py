from django.shortcuts import reverse, get_object_or_404
from django.db.models import Count

from webstore.product.models import Product, Price, Category, Picture

from django_filters.views import FilterView
from django.views import generic

from .forms import ProductFilterForm, PriceCreateForm, PictureFilterForm


class ProductListView(FilterView):
    model = Product
    template_name = 'dashboard/product/product_list.html'
    strict = False
    filterset_class = ProductFilterForm
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.with_prices()


class ProductCreateView(generic.CreateView):
    template_name = 'dashboard/product/product_update.html'
    model = Product
    fields = [
        'name',
        'active',
        'description',
        'weight',
        'width',
        'length',
        'height',
        'categories'
    ]

    def get_success_url(self):
        return reverse('product_panel:product-list')


class ProductUpdateView(generic.UpdateView):
    model = Product
    template_name = 'dashboard/product/product_update.html'
    fields = [
        'name',
        'active',
        'description',
        'weight',
        'width',
        'length',
        'height',
        'categories'
    ]

    def get_success_url(self):
        return reverse('product_panel:product-list')


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


class ProductPriceCreateView(generic.CreateView):
    model = Price
    template_name = 'dashboard/product/product_price_create.html'
    form_class = PriceCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            Product,
            number=self.kwargs.get('number'),
        )
        self.extra_context = {'product': self.product}
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'product': self.product})
        return kwargs

    def get_success_url(self):
        return reverse('product_panel:product-price-list', kwargs={'number': self.product.number})


class PriceUpdateView(generic.UpdateView):
    model = Price
    template_name = 'dashboard/product/product_price_create.html'
    fields = [
        'value',
        'valid_from',
    ]

    def get_success_url(self):
        return reverse('product-price-list', kwargs={'number': self.object.product.numer})

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'dashboard/product/category_list.html'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.all()\
            .annotate(product_count=Count('product'))


class CategoryCreateView(generic.CreateView):
    model = Category
    template_name = 'dashboard/product/category_create_update.html'
    fields = [
        'name',
        'description',
    ]

    def get_success_url(self):
        return reverse('product_panel:category-list')


class CategoryUpdateView(generic.UpdateView):
    model = Category
    template_name = 'dashboard/product/category_create_update.html'
    fields = [
        'name',
        'description',
    ]

    def get_success_url(self):
        return reverse('product_panel:category-list')


class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'dashboard/generic_delete.html'

    def get_success_url(self):
        return reverse('product_panel:category-list')


class PictureListView(FilterView):
    model = Picture
    template_name = 'dashboard/product/picture_list.html'
    paginate_by = 20
    strict = False
    filterset_class = PictureFilterForm


class PictureCreateView(generic.CreateView):
    model = Picture
    fields = [
        'name',
        'data',
    ]
    template_name = 'dashboard/product/picture_create.html'

    def get_success_url(self):
        return reverse('product_panel:picture-list')


class GalleryPicturesListView(generic.ListView):
    # TODO change template
    template_name = 'dashboard/product/picture_list.html'

    def get_queryset(self):
        slug = self.request.resolver_match.kwargs.get('slug')
        return Picture.objects.filter(gallery__product__slug=slug)
