from .models import Cart


def cart_info(request):
    session_id = request.session.session_key
    if session_id is not None:
        cart = Cart.objects.get_or_create(session=session_id)[0]
        cart_item_count = cart.item_count
    else:
        cart_item_count = 0

    if cart_item_count is None:
        cart_item_count = 0

    return {
        "cart_items": cart_item_count,
    }
