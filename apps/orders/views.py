from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, View
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator

from apps.orders.forms import ShippingForm
from apps.orders.models import OrderModel, OrderItemModel
from apps.products.models import ProductModel
from apps.orders.id_generator import make_order_id


class CheckoutCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product-checkout.html'

    def get(self, request, *args, **kwargs):
        form = ShippingForm()
        # Oxirgi user orderini olish
        last_order = OrderModel.objects.filter(user=request.user).last()

        # Agar oxirgi order bo'lmasa, vaqtincha unique_id yaratiladi
        temp_unique_id = last_order.unique_id if last_order else make_order_id()

        context = {
            'form': form,
            'order': last_order,
            'unique_id': temp_unique_id  # HAR DOIM mavjud bo‘ladi
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        basket = request.session.get('basket', {})

        if not basket:
            messages.error(request, "Your cart is empty!")
            return redirect('basket:detail')

        form = ShippingForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Please fill in all required fields correctly.")
            return render(request, self.template_name, {'form': form})

        # Yangi order yaratish
        order = form.save(commit=False)
        order.user = request.user
        order.total_price = 0
        order.total_products = 0
        order.unique_id = make_order_id()
        order.save()

        total_price = 0
        total_products = 0
        not_available = []

        # Savatdagi mahsulotlarni tekshirish va orderga qo‘shish
        for product_id, item_data in basket.items():
            try:
                product = ProductModel.objects.get(id=product_id)
            except ProductModel.DoesNotExist:
                continue

            quantity = item_data.get('quantity', 0)
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
            messages.error(request, f"Out of stock: {', '.join(not_available)}")
            return redirect('basket:detail')

        # Orderga jami narx va mahsulot sonini saqlash
        order.total_price = total_price
        order.total_products = total_products
        order.save()

        # Savatni tozalash
        request.session['basket'] = {}
        request.session.modified = True

        # Payment sahifasiga redirect
        return redirect('orders:payment_page', unique_id=order.unique_id)


def payment_page(request, unique_id):
    # Agar order mavjud bo'lmasa, avtomatik yangi order yaratish
    order, created = OrderModel.objects.get_or_create(
        unique_id=unique_id,
        defaults={'user': request.user, 'total_price': 0, 'total_products': 0}
    )
    context = {
        "order": order,
        "unique_id": order.unique_id
    }
    return render(request, "products/payment.html", context)


@require_POST
def process_payment(request, unique_id):
    order, created = OrderModel.objects.get_or_create(
        unique_id=unique_id,
        defaults={'user': request.user, 'total_price': 0, 'total_products': 0}
    )

    payment_method = request.POST.get('payment_method')
    if payment_method not in dict(OrderModel.PAYMENT_CHOICES):
        messages.error(request, "Invalid payment method selected.")
        return redirect('orders:payment_page', unique_id=unique_id)

    order.payment_method = payment_method
    order.payment_status = 'paid' if payment_method != 'cash' else 'pending'
    order.save()

    messages.success(
        request,
        f"✅ Payment successful via {order.get_payment_method_display()} for order #{order.unique_id}"
    )
    return redirect('products:home')


@method_decorator(require_GET, name='dispatch')
class ProceedToPaymentView(LoginRequiredMixin, View):
    """Tugma bosilganda order yaratish yoki olish va payment sahifasiga redirect"""

    def get(self, request, *args, **kwargs):
        basket = request.session.get('basket', {})

        if not basket:
            messages.error(request, "Your cart is empty!")
            return redirect('basket:detail')

        # Oxirgi orderni olish yoki yangi order yaratish
        order, created = OrderModel.objects.get_or_create(
            user=request.user,
            total_price=0,
            total_products=0,
            defaults={'unique_id': make_order_id()}
        )

        return redirect('orders:payment_page', unique_id=order.unique_id)
