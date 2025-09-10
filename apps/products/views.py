from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Min, Max

from .models import ProductModel, ProductCategoryModel, ManufacturerModel, ProductTagModel, ColorModel

def product_filter_view(request, filter_type=None, pk=None):
    products = ProductModel.objects.filter(status=ProductModel.ProductStatus.PUBLISHED)
    filter_title = ""
    filter_name = ""
    breadcrumbs = []

    selected_child_ids = request.GET.getlist("child")
    selected_manufacturers = request.GET.getlist("manufacturer")
    selected_tags = request.GET.getlist("tag")
    selected_colors = request.GET.getlist("color")
    price_range = request.GET.get("price")


    parent_categories = ProductCategoryModel.objects.filter(parent__isnull=True).annotate(
        product_count=Count("products", distinct=True)
    )
    for parent in parent_categories:
        parent.child_list = parent.children.annotate(
            product_count=Count("products", distinct=True)
        )


    if filter_type == "category" and pk:
        category = get_object_or_404(ProductCategoryModel, id=pk)


        current = category
        while current is not None:
            breadcrumbs.insert(0, current)
            current = current.parent

        filter_title = " > ".join([c.title for c in breadcrumbs])
        if breadcrumbs:
            filter_name = breadcrumbs[-1].title
        else:
            filter_name = ""

        child_categories = category.children.annotate(
            product_count=Count("products", distinct=True)
        )
        if selected_child_ids:
            products = products.filter(category__id__in=selected_child_ids)
        else:
            if child_categories.exists():
                products = products.filter(category__in=child_categories)
            else:
                products = products.filter(category=category)
    else:
        child_categories = ProductCategoryModel.objects.filter(parent__isnull=False).annotate(
            product_count=Count("products", distinct=True)
        )


    manufacturers = ManufacturerModel.objects.all()
    if selected_manufacturers:
        products = products.filter(manufacturer__id__in=selected_manufacturers)


    tags = ProductTagModel.objects.all()
    if selected_tags:
        products = products.filter(tags__id__in=selected_tags).distinct()

    colors = ColorModel.objects.all()
    if selected_colors:
        products = products.filter(color__id__in=selected_colors).distinct()

    min_price = products.aggregate(Min("price"))["price__min"] or 0
    max_price = products.aggregate(Max("price"))["price__max"] or 0
    if price_range:
        try:
            min_val, max_val = map(int, price_range.split(";"))
            products = products.filter(price__gte=min_val, price__lte=max_val)
        except:
            pass

    context = {
        "products": products,
        "filter_title": filter_title,
        "filter_name": filter_name,
        "breadcrumbs": breadcrumbs,
        "parent_categories": parent_categories,
        "child_categories": child_categories,
        "manufacturers": manufacturers,
        "tags": tags,
        "colors": colors,
        "min_price": min_price,
        "max_price": max_price,
        "selected_child_ids": list(map(int, selected_child_ids)),
        "selected_manufacturers": list(map(int, selected_manufacturers)),
        "selected_tags": list(map(int, selected_tags)),
        "selected_colors": list(map(int, selected_colors)),
        "price_range": price_range or f"{min_price};{max_price}",
    }
    return render(request, "products/product-grid-sidebar-left.html", context)



def product_detail_view(request):
    return render(request, 'products/product-detail.html')
