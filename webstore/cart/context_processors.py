from .models import Cart


def cart_info(request):
    session_id = request.session.session_key
    cart_item_count = 0
    if session_id is not None:
        cart = Cart.objects.get_or_create(session_id=session_id)[0]
        cart_item_count = cart.get_item_count()

    return {
        "cart_items": cart_item_count,
    }
