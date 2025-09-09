from django.shortcuts import render
from .models import ProductModel, CategoryModel, ManufacturerModel, ColorModel, TagModel


def product_cart(request):
    return render(request, 'products/product-cart.html')


def product_checkout(request):
    return render(request, 'products/product-checkout.html')


def product_detail(request, pk):
    product = ProductModel.objects.get(pk=pk)
    return render(request, 'products/product-detail.html', {"product": product})


def product_grid_sidebar_left(request, category_id=None):
    products = ProductModel.objects.all()
    categories = CategoryModel.objects.all()
    parent_categories = categories

    manufacturers = ManufacturerModel.objects.all()
    colors = ColorModel.objects.all()
    tags = TagModel.objects.all()

    # Category filter
    if category_id:
        products = products.filter(category_id=category_id)

    # Manufacturer filter
    manufacturer_id = request.GET.get("manufacturer")
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    # Color filter (ManyToMany)
    color_id = request.GET.get("color")
    if color_id:
        products = products.filter(colors__id=color_id)

    # Tag filter (ManyToMany)
    tag_id = request.GET.get("tag")
    if tag_id:
        products = products.filter(tags__id=tag_id)

    return render(request, "products/product-grid-sidebar-left.html", {
        "products": products,
        "categories": categories,
        "parent_categories": parent_categories,
        "manufacturers": manufacturers,
        "colors": colors,
        "tags": tags,
    })
