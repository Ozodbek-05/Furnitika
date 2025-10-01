from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Min, Max, Q

from .models import ProductModel, ProductCategoryModel, ManufacturerModel, ProductTagModel, ColorModel, DealOfTheDayModel

def product_filter_view(request, filter_type=None, pk=None):
    # Barcha PUBLISHED productlar
    products = ProductModel.objects.filter(status=ProductModel.ProductStatus.PUBLISHED)

    filter_title = ""
    filter_name = ""
    breadcrumbs = []

    # GET parametrlari
    selected_child_ids = request.GET.getlist("child")
    selected_manufacturers = request.GET.getlist("manufacturer")
    selected_tags = request.GET.getlist("tag")
    selected_colors = request.GET.getlist("color")
    price_range = request.GET.get("price")

    # Kategoriyalar
    parent_categories = ProductCategoryModel.objects.filter(parent__isnull=True).annotate(
        product_count=Count("products", distinct=True)
    )
    for parent in parent_categories:
        parent.child_list = parent.children.annotate(
            product_count=Count("products", distinct=True)
        )

    child_categories = ProductCategoryModel.objects.filter(parent__isnull=False).annotate(
        product_count=Count("products", distinct=True)
    )

    # Category filter
    if filter_type == "category" and pk:
        category = get_object_or_404(ProductCategoryModel, id=pk)

        # Breadcrumbs
        current = category
        while current is not None:
            breadcrumbs.insert(0, current)
            current = current.parent

        filter_title = " > ".join([c.title for c in breadcrumbs])
        filter_name = breadcrumbs[-1].title if breadcrumbs else ""

        # Tanlangan category va uning barcha child category idlari
        child_categories_ids = list(category.children.values_list('id', flat=True))
        all_category_ids = [category.id] + child_categories_ids

        if selected_child_ids:
            products = products.filter(category__id__in=selected_child_ids)
        else:
            products = products.filter(category__id__in=all_category_ids)

    # Manufacturer filter
    if selected_manufacturers:
        products = products.filter(manufacturer__id__in=selected_manufacturers)

    # Tag filter
    if selected_tags:
        products = products.filter(tags__id__in=selected_tags).distinct()

    # Color filter
    if selected_colors:
        products = products.filter(colors__id__in=selected_colors).distinct()

    # Price filter
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
        "manufacturers": ManufacturerModel.objects.all(),
        "tags": ProductTagModel.objects.all(),
        "colors": ColorModel.objects.all(),
        "min_price": min_price,
        "max_price": max_price,
        "selected_child_ids": list(map(int, selected_child_ids)),
        "selected_manufacturers": list(map(int, selected_manufacturers)),
        "selected_tags": list(map(int, selected_tags)),
        "selected_colors": list(map(int, selected_colors)),
        "price_range": price_range or f"{min_price};{max_price}",
    }

    return render(request, "products/products.html", context)


def product_detail_view(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    return render(request, 'products/product-detail.html',{"product": product})


def deal_of_the_day_view(request):
    now = timezone.now()
    deals = DealOfTheDayModel.objects.filter(
        start_time__lte=now,
        end_time__gte=now
    ).select_related("product")

    context = {
        "deals": deals
    }
    return render(request, "pages/hom3.html", context)


