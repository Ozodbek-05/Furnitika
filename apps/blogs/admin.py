from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.blogs.models import BlogCategoryModel, BlogTagModel, BlogAuthorModel, BlogModel, BlogViewModel

# --- TranslationAdmin uchun baza klass ---
class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

# --- BlogCategoryModel admin ---
@admin.register(BlogCategoryModel)
class BlogCategoryModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['created_at']
    ordering = ['id']

# --- BlogTagModel admin ---
@admin.register(BlogTagModel)
class BlogTagModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['created_at']

# --- BlogAuthorModel admin ---
@admin.register(BlogAuthorModel)
class BlogAuthorModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'full_name']
    search_fields = ['full_name']
    list_filter = ['created_at']
    ordering = ['-id']

# --- BlogModel admin ---
@admin.register(BlogModel)
class BlogModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'title', 'status', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at', 'status']

# --- BlogViewModel admin ---
@admin.register(BlogViewModel)
class BlogViewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_ip', 'blog_title', 'created_at']
    search_fields = ['user_ip']
    list_filter = ['created_at', 'user_ip']
    fields = ['user_ip', 'blog']

    # list_display uchun method
    def blog_title(self, obj):
        return obj.blog.title
    blog_title.admin_order_field = 'blog__title'
    blog_title.short_description = 'Blog Title'
