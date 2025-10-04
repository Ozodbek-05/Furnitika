from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.blogs.models import BlogModel, BlogCategoryModel, BlogTagModel


class BlogListView(ListView):
    template_name = 'blogs/blog-list-sidebar-left.html'

    def get_queryset(self):
        return BlogModel.objects.filter(
            status=BlogModel.BlogStatus.PUBLISHED
        )


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        categories = BlogCategoryModel.objects.all()
        tags = BlogTagModel.objects.all()
        parent_categories = BlogCategoryModel.objects.filter(parent__isnull=True)

        context["blogs"] = self.get_queryset()
        context["categories"] = categories
        context["tags"] = tags
        context["parent_categories"] = parent_categories

        return context



class BlogDetailView(DetailView):
    model = BlogModel
    template_name = "blogs/blog-detail.html"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()

        category = blog.category.first()
        parent_category = category.parent if category else None

        related_blogs = BlogModel.objects.filter(
            category__in=blog.category.all()
        ).exclude(id=blog.id).distinct()[:3]

        context["blogs"] = self.get_queryset()
        context["category"] = category
        context["parent_category"] = parent_category
        context["categories"] = BlogCategoryModel.objects.all()
        context["tags"] = BlogTagModel.objects.all()
        context["parent_categories"] = BlogCategoryModel.objects.filter(parent__isnull=True)
        context["related_blogs"] = related_blogs
        return context



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
        context["tags"] = BlogTagModel.objects.all()
        context["parent_categories"] = BlogCategoryModel.objects.filter(parent__isnull=True)
        return context