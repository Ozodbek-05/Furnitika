from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.db.models import Q

from apps.blogs.models import BlogModel, BlogCategoryModel, BlogTagModel, BlogCommentModel


# --- BLOG SEARCH VIEW ---
class BlogSearchView(ListView):
    model = BlogModel
    template_name = "blogs/blog-list-sidebar-left.html"
    context_object_name = "blogs"

    def get_queryset(self):
        query = self.request.GET.get('s', '').strip()

        if query:
            words = query.split()
            q_objects = Q()
            for word in words:
                q_objects |= (
                        Q(title__icontains=word) |
                        Q(content__icontains=word) |
                        Q(category__title__icontains=word) |
                        Q(tag__title__icontains=word)  # singular tag
                )
            queryset = BlogModel.objects.filter(
                q_objects,
                status=BlogModel.BlogStatus.PUBLISHED
            ).distinct()
        else:
            queryset = BlogModel.objects.filter(status=BlogModel.BlogStatus.PUBLISHED)

        self.search_query = query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = getattr(self, "search_query", "")
        # Sidebar ma’lumotlari
        context["parent_categories"] = BlogCategoryModel.objects.filter(parent__isnull=True)
        context["tags"] = BlogTagModel.objects.all()
        context["recent_blogs"] = BlogModel.objects.filter(
            status=BlogModel.BlogStatus.PUBLISHED
        ).order_by('-created_at')[:5]
        # Header search uchun
        context["search_type"] = "blogs"
        return context


# --- BLOG LIST VIEW ---
class BlogListView(ListView):
    template_name = 'blogs/blog-list-sidebar-left.html'
    context_object_name = "blogs"
    paginate_by = 1

    def get_queryset(self):
        return BlogModel.objects.filter(status=BlogModel.BlogStatus.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_categories"] = BlogCategoryModel.objects.filter(parent__isnull=True)
        context["tags"] = BlogTagModel.objects.all()
        context["recent_blogs"] = BlogModel.objects.filter(
            status=BlogModel.BlogStatus.PUBLISHED
        ).order_by('-created_at')[:5]
        context["search_type"] = "blogs"
        return context


# --- BLOG DETAIL VIEW ---
class BlogDetailView(DetailView):
    model = BlogModel
    template_name = "blogs/blog-detail.html"
    pk_url_kwarg = "pk"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()

        category = blog.category.first()
        parent_category = category.parent if category else None

        related_blogs = BlogModel.objects.filter(
            category__in=blog.category.all()
        ).exclude(id=blog.id).distinct()[:3]

        comments = BlogCommentModel.objects.filter(blog=blog).order_by('-created_at')

        context["category"] = category
        context["parent_category"] = parent_category
        context["related_blogs"] = related_blogs
        context["comments"] = comments

        # Sidebar ma’lumotlari
        context["parent_categories"] = BlogCategoryModel.objects.filter(parent__isnull=True)
        context["tags"] = BlogTagModel.objects.all()
        context["recent_blogs"] = BlogModel.objects.filter(
            status=BlogModel.BlogStatus.PUBLISHED
        ).order_by('-created_at')[:5]

        # Header search uchun
        context["search_type"] = "blogs"

        return context

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        message = request.POST.get('message')

        if name and email and message:
            BlogCommentModel.objects.create(
                blog=blog,
                name=name,
                email=email,
                website=website,
                message=message
            )
            messages.success(request, 'Your comment has been submitted successfully!')
        else:
            messages.error(request, 'Please fill all required fields!')

        return redirect('blogs:detail', pk=blog.pk)


# --- BLOG FILTER VIEW ---
class BlogFilterView(ListView):
    template_name = 'blogs/blog-list-sidebar-left.html'
    context_object_name = "blogs"

    def get_queryset(self):
        filter_type = self.kwargs.get("filter_type")
        pk = self.kwargs.get("pk")
        blogs = BlogModel.objects.filter(status=BlogModel.BlogStatus.PUBLISHED)

        if filter_type == "category":
            try:
                category = BlogCategoryModel.objects.get(id=pk)
                blogs = blogs.filter(category=category)
                self.filter_title = category.title
            except BlogCategoryModel.DoesNotExist:
                raise Http404("Category not found")
        elif filter_type == "tag":
            try:
                tag = BlogTagModel.objects.get(id=pk)
                blogs = blogs.filter(tag=tag)
                self.filter_title = tag.title
            except BlogTagModel.DoesNotExist:
                raise Http404("Tag not found")
        else:
            raise Http404("Invalid filter type")

        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_title"] = getattr(self, "filter_title", "")
        context["filter_type"] = self.kwargs.get("filter_type")

        context["parent_categories"] = BlogCategoryModel.objects.filter(parent__isnull=True)
        context["tags"] = BlogTagModel.objects.all()
        context["recent_blogs"] = BlogModel.objects.filter(
            status=BlogModel.BlogStatus.PUBLISHED
        ).order_by('-created_at')[:5]

        # Header search uchun
        context["search_type"] = "blogs"

        return context
