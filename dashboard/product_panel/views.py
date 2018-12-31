from django.shortcuts import reverse, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django_filters.views import FilterView

from webstore.product.models import (
    Product,
    Price,
    Category,
    Picture,
    Gallery,
)

from .forms import (
    ProductFilterForm,
    PriceCreateForm,
    PictureFilterForm,
    GalleryImageCreateForm,
    GalleryImageChooseForm,
)


class StaffOnlyMixin(UserPassesTestMixin):
    login_url = '/dashboard/users_panel/login'

    def test_func(self):
        return self.request.user.is_staff


class ProductListView(StaffOnlyMixin, FilterView):
    model = Product
    template_name = 'dashboard/product/product_list.html'
    strict = False
    filterset_class = ProductFilterForm
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.with_prices()


class ProductCreateView(StaffOnlyMixin, generic.CreateView):
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


class ProductUpdateView(StaffOnlyMixin, generic.UpdateView):
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


class ProductDeleteView(StaffOnlyMixin, generic.DeleteView):
    model = Product
    template_name = 'dashboard/product/product_delete.html'

    def get_success_url(self):
        return reverse('product_panel:product-list')


class ProductPriceListView(StaffOnlyMixin, generic.ListView):
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


class ProductPriceCreateView(StaffOnlyMixin, generic.CreateView):
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


class PriceUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = Price
    template_name = 'dashboard/product/product_price_create.html'
    fields = [
        'value',
        'valid_from',
        'is_promo',
        'promo_message',
    ]

    def get_success_url(self):
        return reverse('product_panel:product-price-list', kwargs={'number': self.object.product.number})


class CategoryListView(StaffOnlyMixin, generic.ListView):
    model = Category
    template_name = 'dashboard/product/category_list.html'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.all()\
            .annotate(product_count=Count('product'))


class CategoryCreateView(StaffOnlyMixin, generic.CreateView):
    model = Category
    template_name = 'dashboard/product/category_create_update.html'
    fields = [
        'name',
        'description',
    ]

    def get_success_url(self):
        return reverse('product_panel:category-list')


class CategoryUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = Category
    template_name = 'dashboard/product/category_create_update.html'
    fields = [
        'name',
        'description',
    ]

    def get_success_url(self):
        return reverse('product_panel:category-list')


class CategoryDeleteView(StaffOnlyMixin, generic.DeleteView):
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


class PictureCreateView(StaffOnlyMixin, generic.CreateView):
    model = Picture
    fields = [
        'name',
        'data',
    ]
    template_name = 'dashboard/product/picture_create.html'

    def get_success_url(self):
        return reverse('product_panel:picture-list')


class PictureDeleteView(StaffOnlyMixin, generic.DeleteView):
    model = Picture
    template_name = 'dashboard/product/picture_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Picture deleted')
        return reverse('product_panel:picture-list')


class BaseGalleryMixin:

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            klass=Product,
            slug=self.request.resolver_match.kwargs.get('slug'),
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'product': self.product,
        })
        return context

    class Meta:
        abstract = True


class GalleryPicturesListView(BaseGalleryMixin, generic.ListView):
    model = Gallery
    template_name = 'dashboard/product/product_gallery.html'

    def get_queryset(self):
        return self.model.objects.filter(product=self.product).select_related('picture')


class GalleryPicturesUploadView(BaseGalleryMixin, generic.FormView):
    model = Gallery
    template_name = 'dashboard/product/product_gallery_upload.html'
    form_class = GalleryImageCreateForm
    
    def get_form_kwargs(self):
        kwargs = super(GalleryPicturesUploadView, self).get_form_kwargs()
        kwargs.update({
            'product': self.product
        })
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Picture added')
        return reverse(
            viewname='product_panel:product-gallery',
            kwargs={'slug': self.product.slug},
        )

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class GalleryPicturesAddView(BaseGalleryMixin, generic.FormView):
    model = Gallery
    template_name = 'dashboard/product/product_gallery_add.html'
    form_class = GalleryImageChooseForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'product': self.product
        })
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Pictures added')
        return reverse(
            viewname='product_panel:product-gallery',
            kwargs={'slug': self.product.slug},
        )


class GalleryImageRemoveApiView(BaseGalleryMixin, View):
    http_method_names = ['post']
    model = Gallery

    def post(self, *args, **kwargs):
        gallery_image = get_object_or_404(self.model, pk=kwargs.get('pk'))\
                        .delete()
        return HttpResponse(status=204)


class PictureUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = Picture
    template_name = 'dashboard/product/picture/picture_update.html'
    fields = [
        'name',
    ]

    def get_success_url(self):
        messages.info(self.request, 'Picture updated')
        return reverse('product_panel:picture-list')
