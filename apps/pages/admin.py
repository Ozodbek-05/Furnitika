from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from apps.pages.models import ContactModel, BannerModel
admin.site.register(ContactModel)

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


@admin.register(BannerModel)
class BannerAdmin(MyTranslationAdmin):
    list_display = ['title', 'is_active',]
    list_editable = ['is_active']
    search_fields = ['title',]
    list_filter = ['created_at']
