from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from apps.orders.id_generator import make_order_id
from apps.orders.models import OrderModel, OrderItemModel
from apps.products.models import ProductModel


class CheckoutCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product-checkout.html'

    def post(self, request, *args, **kwargs):
        basket = request.session.get('basket', {})

        if not basket:
            messages.error(request, "Your cart is empty!")
            return redirect('basket:detail')

        order = OrderModel.objects.create(
            user=request.user,
            unique_id=make_order_id(length=10),
            total_price=0,
            total_products=0
        )

        total_price = 0
        total_products = 0
        not_available = []

        for product_id, quantity in basket.items():
            try:
                product = ProductModel.objects.get(id=product_id)
            except ProductModel.DoesNotExist:
                continue

            if product.stock < quantity:
                not_available.append(product.title)
                continue

            OrderItemModel.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

            total_price += product.price * quantity
            total_products += quantity

        if not_available:
            order.delete()
            messages.error(
                request,
                f"The following products are out of stock: {', '.join(not_available)}"
            )
            return redirect('basket:detail')

        order.total_price = total_price
        order.total_products = total_products
        order.save()

        request.session['basket'] = {}
        request.session.modified = True

        messages.success(request, "Your order has been successfully placed ✅")
        return redirect('products:home')
