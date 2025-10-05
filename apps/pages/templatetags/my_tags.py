from django import template

from apps.basket.cart import Basket
from apps.wishlist.models import WishlistModel

register = template.Library()


@register.simple_tag
def get_full_url(request, lang):
    path = request.path.split('/')
    path[1] = lang
    return '/'.join(path)


@register.simple_tag
def in_basket(request,product_id):
    basket = Basket(request)
    return basket.in_basket(product_id)


@register.simple_tag
def in_wishlist(request, product_id):
    if request.user.is_authenticated:
        return WishlistModel.objects.filter(user=request.user, product_id=product_id).exists()
    return False