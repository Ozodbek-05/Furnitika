
from django.http import JsonResponse
from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.basket.cart import Basket
from apps.products.models import ProductModel


def basket_detail(request):
    """
    Display the basket contents.
    """
    basket = Basket(request)
    return render(request, 'products/product-cart.html', {'basket': basket})


def basket_add(request, product_id):
    """
    Add a product to the basket.
    """
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)
    quantity = int(request.POST.get('qty', 1))
    basket.add(product=product, quantity=quantity)
    messages.success(request, f'{product.title} added to your basket!')
    return redirect('products:home')


def basket_remove(request, product_id):
    """
    Remove a product from the basket.
    """
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)
    basket.remove(product)
    messages.success(request, f'{product.title} removed from your basket!')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('products:home')


def basket_update(request, product_id):
    if request.method == 'POST':
        basket = Basket(request)
        product = get_object_or_404(ProductModel, id=product_id)
        quantity = int(request.POST.get('qty', 1))

        # Stock check
        if quantity > product.stock:
            return JsonResponse({
                'success': False,
                'message': f'Only {product.stock} available'
            })

        basket.add(product=product, quantity=quantity, override_quantity=True)

        return JsonResponse({
            'success': True,
            'quantity': quantity
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


