from webstore.cart.models import Cart
from webstore.product.models import Category

def cart_info(request):
    cart_item_count = 0
    if request.session.session_key is not None:
        cart = Cart.objects.get_or_create(
            session=request.session.session_key,
        )[0]
        cart_item_count = cart.item_count

    return {
        "cart_items": cart_item_count,
    }


def categories(request):
    return {
        'categories': Category.objects.all()
    }