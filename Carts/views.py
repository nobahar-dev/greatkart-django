from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from Carts.models import Cart, CartItem
from Store.models import Product


def _cart_id(request: HttpRequest):
    my_cart_id = request.session.session_key

    if not my_cart_id:
        my_cart_id = request.session.create()

    return my_cart_id


def add_cart(request: HttpRequest, product_id):
    product: Product = Product.objects.get(id=product_id)

    try:
        my_cart: Cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        my_cart: Cart = Cart.objects.create(cart_id=_cart_id(request))
        my_cart.save()

    try:
        cart_item: CartItem = CartItem.objects.get(product=product, cart=my_cart)
        cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item: CartItem = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=my_cart
        )
        cart_item.save()
    return redirect('cart')


def cart(request, total_price=0, quantity=0, cart_items=None):
    try:
        my_cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items: CartItem = CartItem.objects.filter(cart=my_cart, is_active=True)

        for cart_item in cart_items:
            total_price += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, 'store/carts.html', context)
