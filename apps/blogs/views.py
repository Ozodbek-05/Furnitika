from django.db.models import Count
from django.shortcuts import render

from apps.blogs.models import BlogModel, BlogCategoryModel, BlogTagModel


def blog_list_view(request):
    blogs = BlogModel.objects.filter(
        status=BlogModel.BlogStatus.PUBLISHED
    )
    categories = BlogCategoryModel.objects.all()
    tags = BlogTagModel.objects.all()
    parent_categories = BlogCategoryModel.objects.filter(parent__isnull=True)
    most_popular_blogs = (
        BlogModel.objects
        .annotate(views_count=Count('views', distinct=True))
        .order_by('-views_count')[:4]
    )

    context = {
        "blogs": blogs,
        "categories": categories,
        "tags": tags,
        "parent_categories": parent_categories,
        "most_popular_blogs": most_popular_blogs,
    }
    return render(
        request, 'blogs/blog-list-sidebar-left.html',
        context
    )


def blog_detail_view(request, pk):
    try:
        blog = BlogModel.objects.get(id=pk)
    except BlogModel.DoesNotExist:
        return render(request, 'pages/404.html')

    category = blog.category.first()  # blogning birinchi kategoriyasi
    parent_category = category.parent if category else None

    categories = BlogCategoryModel.objects.all()
    tags = BlogTagModel.objects.all()
    parent_categories = BlogCategoryModel.objects.filter(parent__isnull=True)

    context = {
        'blog': blog,
        'category': category,
        'parent_category': parent_category,
        "categories": categories,
        "tags": tags,
        "parent_categories": parent_categories,
    }
    return render(request, 'blogs/blog-detail.html', context)

