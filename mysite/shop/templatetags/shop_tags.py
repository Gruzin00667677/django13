from django import template
from shop.models import Category, Brand

register = template.Library()


@register.inclusion_tag('shop/cat.html')
def tag_categories():
    category = Category.objects.all()
    return {'category': category}


@register.inclusion_tag('shop/get_filter.html')
def get_filter():
    brands = Brand.objects.all()
    return {'brands': brands}