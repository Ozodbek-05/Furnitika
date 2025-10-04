from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.blogs.models import BlogCategoryModel, BlogTagModel, BlogAuthorModel, BlogModel, BlogViewModel

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

@admin.register(BlogCategoryModel)
class BlogCategoryModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['created_at']
    ordering = ['id']




@admin.register(BlogTagModel)
class BlogTagModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['created_at']


@admin.register(BlogAuthorModel)
class BlogAuthorModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'full_name']
    search_fields = ['full_name']
    list_filter = ['created_at']
    ordering = ['-id']


@admin.register(BlogModel)
class BlogModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'title', 'status', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at', 'status']


@admin.register(BlogViewModel)
class BlogViewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_ip', 'blog__title', 'created_at']
    search_fields = ['user_ip']
    list_filter = ['created_at', 'user_ip']
    fields = ['image', 'title', 'content', 'status', 'author', 'category', 'tag']