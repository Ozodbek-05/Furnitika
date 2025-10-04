from modeltranslation.decorators import register
from modeltranslation.translator import translator, TranslationOptions
from .models import BlogModel, BlogCategoryModel, BlogTagModel, BlogAuthorModel


@register(BlogModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')



@register(BlogTagModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(BlogAuthorModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('full_name', 'bio')


@register(BlogCategoryModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)

