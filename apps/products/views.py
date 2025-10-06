from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count, Min, Max, Q
from .models import (
    ProductModel,
    ProductCategoryModel,
    ManufacturerModel,
    ProductTagModel,
    ColorModel,
    CommentModel,
)


class ProductSearchView(ListView):
    model = ProductModel
    template_name = "products/product-grid-sidebar-left.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('s', '').strip()

        if query:
            words = query.split()
            q_objects = Q()

            for word in words:
                q_objects |= (
                        Q(title__icontains=word) |
                        Q(description__icontains=word) |
                        Q(category__title__icontains=word) |
                        Q(manufacturer__name__icontains=word) |
                        Q(tags__title__icontains=word) |
                        Q(colors__title__icontains=word)
                )

            queryset = ProductModel.objects.filter(
                q_objects,
                status=ProductModel.ProductStatus.PUBLISHED
            ).distinct()
        else:
            queryset = ProductModel.objects.filter(status=ProductModel.ProductStatus.PUBLISHED)

        self.search_query = query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = getattr(self, 'search_query', '')

        context.update({
            "search_query": query,
            "parent_categories": ProductCategoryModel.objects.filter(parent__isnull=True).annotate(
                product_count=Count("products", distinct=True)
            ),
            "child_categories": ProductCategoryModel.objects.filter(parent__isnull=False),
            "manufacturers": ManufacturerModel.objects.all(),
            "tags": ProductTagModel.objects.all(),
            "colors": ColorModel.objects.all(),
            "selected_child_ids": [],
            "selected_manufacturers": [],
            "selected_tags": [],
            "selected_colors": [],
            "empty_message": f'No products found for "{query}"' if query and not context['products'] else '',
        })
        return context


class ProductFilterView(ListView):
    model = ProductModel
    template_name = "products/product-grid-sidebar-left.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        queryset = ProductModel.objects.filter(status=ProductModel.ProductStatus.PUBLISHED)

        filter_type = self.kwargs.get("filter_type")
        pk = self.kwargs.get("pk")

        selected_child_ids = self.request.GET.getlist("child")
        selected_manufacturers = self.request.GET.getlist("manufacturer")
        selected_tags = self.request.GET.getlist("tag")
        selected_colors = self.request.GET.getlist("color")
        price_range = self.request.GET.get("price")

        if filter_type == "category" and pk:
            category = get_object_or_404(ProductCategoryModel, id=pk)
            child_categories = category.children.all()
            if child_categories.exists():
                queryset = queryset.filter(category__in=[category, *child_categories])
            else:
                queryset = queryset.filter(category=category)
            self.category = category
        else:
            self.category = None

        if filter_type == "tag" and pk:
            selected_tags = [pk]

        if selected_manufacturers:
            queryset = queryset.filter(manufacturer__id__in=map(int, selected_manufacturers))
        if selected_tags:
            queryset = queryset.filter(tags__id__in=map(int, selected_tags)).distinct()
        if selected_colors:
            queryset = queryset.filter(colors__id__in=map(int, selected_colors)).distinct()

        min_price = ProductModel.objects.aggregate(Min("price"))["price__min"] or 0
        max_price = ProductModel.objects.aggregate(Max("price"))["price__max"] or 0
        if price_range:
            try:
                min_val, max_val = map(int, price_range.split(";"))
            except:
                min_val, max_val = int(min_price), int(max_price)
        else:
            min_val, max_val = int(min_price), int(max_price)
        queryset = queryset.filter(price__gte=min_val, price__lte=max_val)

        self.min_price = min_price
        self.max_price = max_price

        if not queryset.exists():
            self.empty_message = "No products found for your selected filters."
        else:
            self.empty_message = ""

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = []
        category = getattr(self, "category", None)
        if category:
            current = category
            while current:
                breadcrumbs.insert(0, current)
                current = current.parent

        context.update({
            "breadcrumbs": breadcrumbs,
            "parent_categories": ProductCategoryModel.objects.filter(parent__isnull=True).annotate(
                product_count=Count("products", distinct=True)
            ),
            "child_categories": ProductCategoryModel.objects.filter(parent__isnull=False),
            "manufacturers": ManufacturerModel.objects.all(),
            "tags": ProductTagModel.objects.all(),
            "colors": ColorModel.objects.all(),
            "selected_child_ids": list(map(int, self.request.GET.getlist("child"))),
            "selected_manufacturers": list(map(int, self.request.GET.getlist("manufacturer"))),
            "selected_tags": list(map(int, self.request.GET.getlist("tag"))),
            "selected_colors": list(map(int, self.request.GET.getlist("color"))),
            "min_price": getattr(self, "min_price", 0),
            "max_price": getattr(self, "max_price", 0),
            "price_range": self.request.GET.get(
                "price",
                f"{int(getattr(self, 'min_price', 0))};{int(getattr(self, 'max_price', 0))}"
            ),
            "empty_message": getattr(self, "empty_message", ""),
        })
        return context


class ProductDetailView(DetailView):
    template_name = "products/product-detail.html"
    queryset = ProductModel.objects.all()
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context['category'] = product.category
        context['parent_category'] = product.category.parent if product.category else None
        context['related_products'] = ProductModel.objects.filter(
            category=product.category,
            status=ProductModel.ProductStatus.PUBLISHED
        ).exclude(id=product.id)[:3]
        context['best_sellers'] = ProductModel.objects.filter(
            status=ProductModel.ProductStatus.PUBLISHED
        ).order_by('-rating')[:3]
        context['all_tags'] = ProductTagModel.objects.all()
        context['all_categories'] = ProductCategoryModel.objects.filter(parent__isnull=True)
        context['comments'] = CommentModel.objects.filter(product=product).order_by('-created_at')

        return context


class CommentCreateView(CreateView):
    model = CommentModel
    fields = ['name', 'email', 'comment']

    def form_valid(self, form):
        product = get_object_or_404(ProductModel, pk=self.kwargs['pk'])
        form.instance.product = product
        form.save()
        return redirect('products:detail', pk=product.pk)


class LivingRoomProductsView(ListView):
    model = ProductModel
    template_name = "products/product-grid-sidebar-left.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        living_room_category = get_object_or_404(
            ProductCategoryModel,
            title__iexact="Living Room"
        )

        queryset = ProductModel.objects.filter(
            category=living_room_category,
            status=ProductModel.ProductStatus.PUBLISHED
        )

        # DEBUG
        print(f"🔍 Living Room products count: {queryset.count()}")
        for product in queryset[:3]:
            print(f"   - {product.title}")
            print(f"     Image: {product.image.url if product.image else 'NO IMAGE'}")
            print(f"     Price: {product.price}")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # DEBUG
        print(f"🔍 Context products count: {len(context['products'])}")
        context.update({
            "parent_categories": ProductCategoryModel.objects.filter(parent__isnull=True),
            "manufacturers": ManufacturerModel.objects.all(),
            "tags": ProductTagModel.objects.all(),
            "colors": ColorModel.objects.all(),
        })
        return context