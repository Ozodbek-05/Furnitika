from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import ContactModel


@register(ContactModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('subject', 'message')
