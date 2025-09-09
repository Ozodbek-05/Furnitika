from django import template

register = template.Library()

@register.simple_tag
def get_full_url(request, lang):
    path = request.path.split('/')
    if len(path) > 1:
        path[1] = lang
    return '/'.join(path)
