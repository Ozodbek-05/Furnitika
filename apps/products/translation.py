from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import ProductModel, ProductCategoryModel, ProductTagModel, ColorModel, ManufacturerModel


@register(ProductModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(ProductCategoryModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(ProductTagModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ColorModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(ManufacturerModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', )