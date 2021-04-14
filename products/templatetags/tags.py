from django import template

from products.models import Category, Brand

register = template.Library()


@register.inclusion_tag('categories_brands.html')
def show_categories_brands(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return {'categories': categories,
            'brands': brands,
            'request': request}


