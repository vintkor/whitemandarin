# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template import Context, loader
from django.core.cache import cache
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import never_cache, cache_page
from django.db.models import Q

from content.models import *
from shop.models import Product, Articles, Order
from profile.models import User

def update_date(list):
    return [list[i:i+2] for i in range(0, len(list), 2)]

def my_404_view(request):
    template = loader.get_template('404.html')
    context = Context({
        'request': request,
    })
    return HttpResponse(
        content=template.render(
            context), content_type='text/html; charset=utf-8', status=404)


def clear_cache(request):
    cache.clear()
    products = Product.objects.all()
    for product in products:
        product.colors = None
        product.save()
    return redirect('/')


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def e(request):
    users = Order.objects.all()
    for u in users:
        try:
            uu = User.objects.get(email=u.email)
        except:
            if u.email:
                uu = User.objects.create_user(email=u.email, username=u.email, password='12345')
                uu.phone = u.phone
                uu.first_name = u.name

            uu.save()
    return HttpResponse("ok")

# @cache_page(60 * 60 * 24)
@never_cache
def home(request):


    if request.get_full_path().strip('?')[0][-5:] == "/amp/":
        print 'd'
    
    # assert False, request.session['compare']
    actions = Product.objects.filter(
        action=1, price__gt=0, published=1).order_by('?')
    qt_actions = actions.count()
    actions = actions[:12]

    bests = Product.objects.filter(
        Q(action=1) | Q(oldprice__gt=0), price__gt=0, published=1
    ).order_by('-id')[:12]

    qt_sales = Product.objects.filter(
        oldprice__gt=0, price__gt=0, published=1).count()
    # assert False, qt_sales

    ids = []
    for i in actions:
        ids.append(i.id)

    new = Product.objects.filter(
        newproduct=1, price__gt=0, published=1
    ).exclude(id__in=ids).order_by('?')[:12]
    # assert False, new

    popular = Product.objects.filter(
        price__gt=0, published=1).order_by('-count_views')[:12]

    items_id = []
    # dict_values = []
    try:
        for item in dict.values(request.session['compare']):
            for i in item:
                items_id.append(i)
    except:
        pass
    
    slid = None
    verview = None
    category = None
    if  "/amp/" in request.get_full_path():
        from slideshow.models import Slid
        slid = Slid.objects.filter(category_id=4).order_by('ordering')
        from content.models import Article
        verview = Article.objects.filter(category_id=3, published=1).order_by('-pub_date')[:3]
        from shop.models import Category
        category = Category.objects.filter(parent=None, published=True).order_by('ordering')
        new = update_date(new)
        bests = update_date(bests)
        popular = update_date(popular)
        html = 'index_amp.html'
    else:
        html = 'index.html'
    
    print category

    return render(request, html, {
        # 'actions': actions,
        'bests': bests,
        'new': new,
        'popular': popular,
        'items_id': items_id,
        'qt_actions': qt_actions,
        'qt_sales': qt_sales,
        "slid":slid,
        "verview":verview,
        "category":category,
    })


def page(request, slug):

    for l in slug:
        if l.isupper():
            return HttpResponsePermanentRedirect('/page/' + slug.lower() + '/')

    page = get_object_or_404(Article, slug=slug)

    if page.category_id == 3 and 'page' in request.get_full_path():
        return HttpResponsePermanentRedirect('/overviews/' + slug.lower() + '/')

    return render(request, 'content/page.html', {'page':page})


def akcii(request):
    category = get_object_or_404(Category, slug='akcii')
    pages = Article.objects.filter(category=category)
    return render(request, 'content/akcii.html', {'pages':pages, 'category':category})


def akcya(request, slug):
    page = get_object_or_404(Article, slug=slug)
    return render(request, 'content/akcya.html', {'page':page})


def usfull(request):
    items = Articles.objects.filter(published=1)
    return render(request, 'content/usful.html', {'items':items})


def usfull_item(request,slug):

    for l in slug:
        if l.isupper():
            return HttpResponsePermanentRedirect('/usfull/' + slug.lower() + '/')

    item = get_object_or_404(Articles, slug=slug)
    return render(request, 'content/usful_item.html', {'page':item})


def google(request):
    return render(request, 'content/google.html')


def robots(request):
    return HttpResponse('User-agent: *\nDisallow: /checkout/\nDisallow: /search/\nHost: https://20k.com.ua\nSitemap: https://20k.com.ua/20k.xml', content_type="text/plain")


@never_cache
def overviews(request):

    category = get_object_or_404(Category, pk=3)
    items = Article.objects.filter(category=category).order_by('-pub_date')

    # assert False, items
    return render(request, 'content/overviews.html', {'items':items})
