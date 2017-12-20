# -*- coding: utf-8 -*-
from content.models import *
from shop.models import *
from django import template
register = template.Library()


@register.inclusion_tag('tags/megamenu.html')
def megamenu(request):
    items = Category.objects.filter(level=0)
    # assert False, items
    return {'items':items, 'request': request}



@register.inclusion_tag('tags/htmlcode.html')
def htmlcode(id):
    item = Snipet.objects.get(pk=id)
    return {'item':item,}



@register.inclusion_tag('tags/product.html')
def product(request, item, small=False):
    return {'item':item, 'request': request, 'small':small}




@register.inclusion_tag('tags/menus.html')
def menus(request):

    items = MenuItem.objects.filter(menu_id=1, published=True).order_by("ordering")
    return {'items':items, 'request': request}




@register.inclusion_tag('tags/topcategory.html')
def topcategory(request):
    items = Category.objects.filter(top=True)
    return {'items':items, 'request': request}




@register.inclusion_tag('tags/topbrand.html')
def topbrand(request):
    items = Brand.objects.filter(top=True)
    return {'items':items, 'request': request}


