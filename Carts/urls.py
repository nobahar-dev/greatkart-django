from django.urls import path

from Carts import views

urlpatterns = [
    path('', views.cart, name='cart')
]
