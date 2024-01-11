from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from Category.models import Category
from Store.models import Product


def store(request: HttpRequest, category_slug=None):
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    context = {'products': products, 'product_count': products_count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as ex:
        raise ex

    context = {'product': product}
    return render(request, 'store/product_detail.html', context)
