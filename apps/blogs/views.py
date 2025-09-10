from django.shortcuts import render


from apps.blogs.models import BlogModel, BlogCategoryModel, BlogTagModel


def blog_list_view(request):
    blogs = BlogModel.objects.filter(
        status=BlogModel.BlogStatus.PUBLISHED
    )
    tags = BlogTagModel.objects.all()
    parent_categories = BlogCategoryModel.objects.filter(parent__isnull=True)


    context = {
        "blogs": blogs,
        "tags": tags,
        "parent_categories": parent_categories
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
    
    category = blog.category.first()
    parent_category = category.parent if category else None

    related_blogs = BlogModel.objects.filter(
        category__in=blog.category.all()
    ).exclude(id=blog.id).distinct()[:3]


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
        'related_blogs': related_blogs
    }
    return render(request, 'blogs/blog-detail.html', context)


def blog_filter_view(request, filter_type, pk):
    blogs = BlogModel.objects.filter(status=BlogModel.BlogStatus.PUBLISHED)
    filter_title = ""

    if filter_type == "category":
        try:
            category = BlogCategoryModel.objects.get(id=pk)
            blogs = blogs.filter(category=category)
            filter_title = category.title
        except BlogCategoryModel.DoesNotExist:
            return render(request, "pages/404.html")

    elif filter_type == "tag":
        try:
            tag = BlogTagModel.objects.get(id=pk)
            blogs = blogs.filter(tag=tag)
            filter_title = tag.title
        except BlogTagModel.DoesNotExist:
            return render(request, "pages/404.html")

    else:
        return render(request, "pages/404.html")

    tags = BlogTagModel.objects.all()
    parent_categories = BlogCategoryModel.objects.filter(parent__isnull=True)

    context = {
        "blogs": blogs,
        "filter_title": filter_title,
        "filter_type": filter_type,   # ⬅️ BU YO'Q EDI, QO‘SHILDI
        "tags": tags,
        "parent_categories": parent_categories,
    }
    return render(request, "blogs/blog-list-sidebar-left.html", context)
