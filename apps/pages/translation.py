from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import ContactModel, BannerModel


@register(ContactModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('subject', 'message', )


@register(BannerModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)

