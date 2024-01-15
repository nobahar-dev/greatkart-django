from django.http import HttpRequest

from Carts.models import Cart, CartItem
from Carts.views import _cart_id


def cart_counter(request: HttpRequest):
    cart_count = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            my_cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            cart_items = CartItem.objects.all().filter(cart=my_cart)

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            pass
        return dict(cart_count=cart_count)
