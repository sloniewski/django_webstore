from django.views.generic import TemplateView
from webstore.product.models import Category, Product


class WelcomeView(TemplateView):
    template_name = 'webstore/core/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.with_products(),
            'promo_prod': Product.objects.with_prices().filter(is_promo=True)[:8],
            'newcomers': Product.objects.newcomers().with_prices()[:8],
        })
        return context

