from django import template

from products.models import Category

register = template.Library()


@register.inclusion_tag('categories.html')
def show_category(request):
    categories = Category.objects.all()
    return {'categories': categories,
            'request': request}
