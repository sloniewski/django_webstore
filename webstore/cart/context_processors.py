from .models import Cart


def cart_info(request):
    cart_item_count = 0
    if request.session.session_key is not None:
        cart = Cart.objects.recive_or_create(request)
        cart_item_count = cart.item_count

    return {
        "cart_items": cart_item_count,
    }
