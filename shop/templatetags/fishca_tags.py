# -*- coding: utf-8 -*-
from django import template
register = template.Library()
from shop.models import *
from comments.models import *
import copy
from django.shortcuts import get_object_or_404


@register.filter
def multiply(string, times):
    return string * times


@register.filter(name='private')
def private(obj, attribute):
    return obj[attribute]

def my_app_name(app_name):
    try:
        app = __import__(app_name.lower())
        return app.app_label
    except:
        return app_name

my_app_name = register.simple_tag(my_app_name)


@register.filter
def thumb(value):
    value = str(value)
    parts = value.split(".")
    parts.insert(-1, "thumb")
    return ".".join(parts)

@register.filter
def clearskobki(value):
    value = value.replace('(', '').replace(')', '')
    # parts = value.split(".")
    # parts.insert(-1, "thumb")
    return value


@register.filter
def removenbsp(value):
    value = value.replace('&nbsp;',' ')
    return value

@register.filter
def cut_name(value):
    return value[:25]


@register.filter
def withoutnull(value):
    if value:
        return str(int(value))
    else:
        return ''



@register.inclusion_tag('tags/abf.html')
def abf(category, active_brands, active_filters, ab, af):
    items = []
    bcopy = copy.copy(active_brands)
    fcopy = copy.copy(active_filters)
    if ab:
        name = get_object_or_404(Brand, id=ab).name
        bcopy.remove(ab)
    if af:
        fi = get_object_or_404(FilterSelect, id=af)
        name = fi.filter.name + ": " + fi.value
        fcopy.remove(af)

    for b in bcopy:
        items.append('brand_' + str(b) + '=1')


    for f in fcopy:
        items.append('prop_' + str(f) + '=1')

    npath = "&".join(items)

    url = "/" + category.slug + "/?" + npath


    return {'name':name, 'url': url}


@register.inclusion_tag('tags/snipet.html')
def snipet(f=1):
    from content.models import Snipet
    snipet = Snipet.objects.get(id=f)
    return {'snipet':snipet}


@register.inclusion_tag('tags/menu.html')
def menu(f=1):
    from content.models import MenuItem
    items = MenuItem.objects.filter(menu_id=int(f), published=1).order_by('ordering')
    return {'items':items}


@register.inclusion_tag('tags/search_cat.html')
def scats(f=1):
    from shop.models import Category
    # items = Category.objects.filter(published = 1, level = 0).exclude(id = 998).order_by('ordering')
    items = []
    return {'items':items}


@register.inclusion_tag('tags/top_menu.html')
def topMenu(request):
    from shop.models import Category
    items = items = Category.objects.filter(parent=None, published=True).order_by('ordering')
    cat = Category.objects.filter(published=1).order_by('ordering')

    return {'items': items, 'request': request, 'cat': cat}


@register.inclusion_tag('tags/top_menu.html')
def topMenu2(request):
    from shop.models import Category
    cat = Category.objects.filter(published=1).order_by('ordering')

    return {'cat': cat, 'request': request}


@register.inclusion_tag('tags/product_left.html')
def product_left(product, category, seo_pages=[], seo_brand=[]):
    brands = Product.objects.filter(category = product.category).values('brand').distinct()

    brand_ids_in = []

    for brand in brands:
        brand_ids_in.append(brand['brand'])

    result_brands = Brand.objects.filter(pk__in = brand_ids_in).order_by('name')

    result = []

    for item in result_brands:
        # assert False, item.slug
        one = { 'id': item.id, 'brand': item, 'products': item.products(product.category), 'slug': item.slug}
        result.append(one)



    return {"items": result, "product": product, "category": category, 'seo_pages':seo_pages, 'seo_brand':seo_brand}

@register.inclusion_tag('tags/brand_left.html')
def brand_left(brand, category, low_price=[], popular=[], seo_brand=[]):

    brands = category.get_brands
    # assert False, brands

    return {"brands": brands, "brand": brand, "category": category, 'low_price':low_price, 'popular':popular, 'seo_brand':seo_brand}


@register.inclusion_tag('tags/top_slide.html')
def top_slide():
    from slideshow.models import Slid
    try:
        static_item = Slid.objects.filter(category_id=3)[0]
    except:
        static_item = None

    items = Slid.objects.filter(category_id=4).order_by('ordering')
    items_id = []
    # dict_values = []
    try:
        for item in dict.values(request.session['compare']):
            for i in item:
                items_id.append(i)
    except:
        pass
    return {'items': items, 'items_id': items_id, 'static_item': static_item}


@register.inclusion_tag('tags/desktop.html')
def descktop_menu(request):
    from shop.models import Category
    items = Category.objects.filter(parent=None, published=True).order_by('ordering')

    return {'items': items, 'request': request}


@register.inclusion_tag('tags/top_prod.html')
def top_prod(c, type='cat'):
    from shop.models import Product

    child_categories = Category.objects.filter(parent=c)
    if child_categories:
        items = Product.objects.filter(
            category__in=child_categories, published=1, action=1, price__gt=0
        ).order_by('?')[:12]
        # assert False, items
    else:
        items = Product.objects.filter(
            category=c, published=1, action=1, price__gt=0
        ).order_by('?')[:12]

    if not items:
        items = Product.objects.filter(
            category__parent=c, published=1, action=1, price__gt=0
        ).order_by('?')[:12]

    return {'items': items, 'type': type}


@register.inclusion_tag('tags/similar_prod.html')
def similar_prod(c):
    from shop.models import Product

    items = Product.objects.filter(
        category=c, published=1, price__gt=0
    ).order_by('?')[:12]

    return {'items': items}


@register.inclusion_tag('tags/last_overviews.html')
def last_overviews():
    from content.models import Article

    items = Article.objects.filter(category_id=3, published=1).order_by('-pub_date')[:3]

    return {'items': items}


@register.inclusion_tag('tags/main_prod.html')
def main_prod():
    from shop.models import Product
    items = Product.objects.filter(action=1, published=1, price__gt=0).order_by('-id')[:3]
    return {'items':items}


    # assert False, result_brands

@register.inclusion_tag('tags/usfull.html')
def usfull(c):
    from shop.models import Articles
    items = Articles.objects.filter(category=c, published=1)[:3]
    return {'items':items}


@register.inclusion_tag('tags/product.html')
def product(one, items_id, type='cat', nofollow=False):
    return {'one': one, 'items_id': items_id, 'type': type, "nofollow":nofollow}

@register.simple_tag
def abrands(brands, active_brands):
    results = []

    for b in brands:
        if b.id in active_brands:
            results.append(b.name)

    if results:
        return ", ".join(results)

    return ""


@register.simple_tag
def afilters(filters, active_filters):
    results = []

    for f in filters:
        if f.id in active_filters:
            results.append(f.value)

    if results:
        return ", ".join(results)

    return ""




@register.inclusion_tag('tags/showbrand.html')
def showbrand(category, active_brands, active_filters, one):
    # assert False, one

    newone = {}
    newone['id'] = one.id
    newone['value'] = one.name
    newone['url'] = False
    if not active_brands:
        key = "brand_" + str(one.id)

        if active_filters:
            for f in active_filters:
                key += 'prop_' + str(f)
            # assert False, key

        # assert False,
        if key in category.getseo:
            newone['slug'] = category.getseo[key]
#     def getcount(self, active_brands, active_filters, one_brand = False, one_filter = False):


    # count = category.getcount(active_brands, active_filters, one.id)

    # assert False, newone
    return {'one': newone, 'category': category, 'active_brands': active_brands, 'active_filters': active_filters}


@register.inclusion_tag('tags/showfilter.html')
def showfilter(category, active_brands, active_filters, one):
    # assert False, one

    newone = {}
    newone['id'] = one.id
    newone['value'] = one.value
    newone['slug'] = False
    if len(active_brands) <= 1 and len(active_filters) < 3:
        key = ""
        if active_brands:
            key += "brand_" + str(active_brands[0])

        fils = copy.deepcopy(active_filters)
        if not fils:
            fils = []

        fils.append(one.id)
        fils.sort()

        # assert False, fils

        for fil in fils:
            key += "prop_" + str(fil)

        if key in category.getseo:
            newone['slug'] = category.getseo[key]
            # assert False, newone

    # count = category.getcount(active_brands, active_filters, False, one.id)
        # assert False, count
    # assert False, newone
    return {'one': newone, 'category': category, 'active_brands': active_brands, 'active_filters': active_filters}

@register.inclusion_tag('tags/createseo.html')
def createseo(item):

    try:

        url = item.get_url
        if item.category:
            categories = item.category.allnames
        else:
            categories = []
        colors = item.get_colors

        if item.brand:
            brand = item.brand.name
        else:
            brand = ""
        names = item.name.split(brand)
        if len(names) > 1:
            name = names[1]
        else:
            name = item.name

        keys = [u'купить', u'отзывы', u'описание']
        return {'url': url, 'categories': categories, 'colors': colors, 'brand': brand, 'keys': keys, 'name': name,}
    # colors
    # categories
    # brand
    # name
    # keys

    except Exception, e:
        pass

@register.inclusion_tag('tags/seocomment.html')
def seocomment(category, brand=None):
    p = Product.objects.filter(category=category)
    print p
    if not p:
        p = Product.objects.filter(category__parent=category)
    if not p:
        p = Product.objects.filter(category__parent__parent=category)
    if brand:
        p = p.filter(brand=brand)
    ids = [z.id for z in p]
    comments = Comments.objects.filter(item_id__in=ids, published_in_category=True)[:4]
    print brand
    return {'comments':comments, "category":category, 'brand':brand}
