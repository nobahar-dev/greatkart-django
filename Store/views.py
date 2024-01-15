from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from Carts.models import CartItem
from Carts.views import _cart_id
from Category.models import Category
from Store.models import Product


def store(request: HttpRequest, category_slug=None):
    paged_products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available=True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    context = {'products': paged_products, 'product_count': products_count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as ex:
        raise ex

    context = {'product': product, 'in_cart': in_cart}
    return render(request, 'store/product_detail.html', context)


def search(request: HttpRequest):
    products = None
    product_count = None

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(descriptions__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {'products': products, 'product_count': product_count}
    return render(request, 'store/store.html', context)
