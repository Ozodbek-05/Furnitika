from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.basket.cart import Basket
from apps.products.models import ProductModel


def basket_detail(request):
    """
    Display the basket contents.
    """
    basket = Basket(request)
    return render(request, 'products/cart.html', {'basket': basket})


def basket_add(request, product_id):
    """
    Add a product to the basket.
    """
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)

    basket.add(product=product, quantity=1)
    messages.success(request, f'{product.title} added to your basket!')
    return redirect('products:list')


def basket_remove(request, product_id):
    """
    Remove a product from the basket.
    """
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)
    basket.remove(product)
    messages.success(request, f'{product.title} removed from your basket!')
    return redirect('products:list')
