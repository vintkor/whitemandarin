# -*- coding: utf-8 -*-
# from django.db import models
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.template import Context, loader
# from django.views.decorators.cache import cache_page
# from django.core.cache import cache
from django.shortcuts import redirect, render, get_object_or_404
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# from django.utils import simplejson
from django.views.decorators.cache import never_cache, cache_page
from .models import *
import json
import datetime
import base64
import random
from django.contrib.auth import authenticate, login
import csv
import StringIO
from django.utils.encoding import smart_unicode
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test


from shop.models import *
# from cms.local_settings import PROJECT_PATH
from discount.settings import BASE_DIR
import codecs
import json
from django.template import loader, Context
import codecs

from django.core.cache import cache

# import unicodecsv
# from easy_thumbnails.files import get_thumbnailer
@user_passes_test(lambda u: u.is_admin)
@never_cache
def allactions(request):
    return render(request, 'allactions.html', {})


@never_cache
@user_passes_test(lambda u: u.is_staff)
def clearcache(request):
    cache.clear()
    return HttpResponse('ok')


@user_passes_test(lambda u: u.is_admin)
@never_cache
def createmenu(request):
    items = Category.objects.filter(published=1, parent=None).order_by('ordering')

    template = loader.get_template('tags/desktop.html')

    body_html = template.render(Context({'items': items}))

    file = codecs.open(BASE_DIR + '/discount/templates/include/desktop.html', "w", "utf-8")
    file.write(body_html)
    file.close()

    template = loader.get_template('tags/top_menu.html')

    body_html = template.render(Context({'items': items}))

    file = codecs.open(BASE_DIR + '/discount/templates/include/mobile.html', "w", "utf-8")
    file.write(body_html)
    file.close()

    return HttpResponse("ok")

@user_passes_test(lambda u: u.is_admin)
@never_cache
def getactionbycat(request, id):
    items = Product.objects.filter(category_id=id, published=True, price__gt=0)
    aitems = Product.objects.filter(category_id=id, published=True, price__gt=0, action=True)
    itemsresult = []
    aitemsresult = []
    for item in items:
        itemsresult.append({'id': item.id, 'name': item.name })

    for item in aitems:
        aitemsresult.append({'id': item.id, 'name': item.name, 'actionname': item.action_name })
    data = {
        'items': itemsresult,
        'aitems': aitemsresult,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

  #   pass


@user_passes_test(lambda u: u.is_admin)
@never_cache
def setaction(request):
    ids = request.POST.get('ids', 0).split(',')
    name = request.POST.get('name', '')
    date = request.POST.get('date', '')
    # recomendproduct = request.POST.get('recomendproduct', '').split(',')

    if date:
        date = datetime.datetime.strptime(date, '%d.%m.%Y')

    if ids[0]:
        for id in ids:
            product = Product.objects.get(pk=id)
            if name:
                product.action_name = name
                product.action_time = date
                product.action = True
            else:
                product.action_name = ""
                product.action_time = None
                product.action = False

            product.save()


    return HttpResponse('ok')


@never_cache
def seopage(request):
    items = Product.objects.filter(published=True, price__gt=0)
    return render(request, 'shop/seopage.html',{'items': items})
        # assert False, itemsxs

@never_cache
def seometa(request):
    items = Product.objects.filter(published=True, price__gt=0)
    return render(request, 'shop/seometa.html',{'items': items})
    pass

@never_cache
def seokey(request):
    items = Product.objects.filter(published=True, price__gt=0)
    return render(request, 'shop/seokey.html',{'items': items})
    pass


@never_cache
def delete_phrase(request):
    item = get_object_or_404(EcomercePhrase, pk = int(request.POST.get('id')))
    item.active = False
    item.save()
    data = json.dumps('ok')
    return HttpResponse(data, content_type="application/json")


@never_cache
def get_one_node(request):
    item = get_object_or_404(Ecomerce, pk = int(request.POST.get('id')))

    result = {
        'name': item.name,
        'phrases': [],
    }

    for phrase in item.phrases():
        result['phrases'].append({
            'id' : phrase.id,
            'name' :phrase.name,
            'frequency_google' : phrase.frequency_google,
            'frequency_yandex' : phrase.frequency_yandex,
            'nowposition_google' : phrase.nowposition_google,
            'nowposition_yandex' : phrase.nowposition_yandex,
            'lastposition_google': phrase.lastposition_google,
            'lastposition_yandex': phrase.lastposition_yandex,
            'nofound' : phrase.nofound,
        })
    # pass

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")




@never_cache
def writecaptcha(request):
    items = EcomerceCaptcha.objects.filter(response__isnull = True)
    if request.is_ajax():

        results = []
        if items:
            for item in items:
                results.append({'request': item.request, 'id': item.id})


        data = json.dumps(results)

        return HttpResponse(data, content_type="application/json")



    else:
        if request.method == 'POST':
            for item in items:
                response = request.POST.get('response_' + str(item.id), '')
                # assert False, response
                if response:
                    item.response = response
                    item.save()
            return HttpResponsePermanentRedirect('/writecaptcha/')
        else:
            return render(request, 'ecommerce/writecaptcha.html',{'items': items})
        # assert False, itemsxs


@never_cache
def importcsv(request):
    csvdata = request.POST.get('csv', '').encode('utf-8')
    url_id = int(request.POST.get('url_id', 0))
    result = []
    for row in csvdata.split('\n'):
        name = row.split(',')[0]

        if not EcomercePhrase.objects.filter(name=name):
            data = {'name': name}
            if url_id:

                url = get_object_or_404(Ecomerce, pk=url_id)
                data['url'] = url
            ecom = EcomercePhrase(**data)
            ecom.save()

            result.append(name)

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")


@never_cache
def get_nodes(request):
    id = request.GET.get('id', 0)
    try:
        id = int(id)
        data = {'parent_id': id}
    except:
        data = {'level': 0}
        # id = False
    items = Ecomerce.objects.filter(**data)
    result = []
    for item in items:
        result.append({
                'text': item.name,
                'id': item.id,
                'children': item.is_child()
            })

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")


@never_cache
def ecomerce(request):
    items = Ecomerce.objects.all()

    return render(request, 'ecommerce/ecommerce.html', {'items': items})

def manager(request):
    if not request.user.is_authenticated() and request.user.is_admin:
        redirect('/')

    if request.method == 'POST':

        color_idname = request.POST.get('color_id', False)

        if color_idname:
            color = ColorProduct.objects.filter(idname__icontains = color_idname)

        if color:
            color = color[0]
            statistica = Statistica(user = request.user, session_id = request.POST.get('session_id'), color = color)
            statistica.pub_date = datetime.datetime.now()
            statistica.save()
            return HttpResponsePermanentRedirect(color.get_url())

        else:

            error = "Вы ввели не правильный код товара"

    return render(request, 'shop/manager.html')



def sitemap(request):
    categorys = Category.objects.filter(published=1)
    prods = Product.objects.filter(published=1)
    seo = Seo.objects.all()
    seo_brand = SeoBrand.objects.all()
    popular = Popular.objects.all()
    nedorogo = LowPrice.objects.all()
    catbrands = FilterSeo.objects.all()
    return render(request, 'shop/google_sitemap.html', {
        "categorys":categorys,
        "catbrands": catbrands,
        # 'seo_brand':seo_brand,
        # 'seo':seo,
        'prods':prods,
        # 'popular':popular,
        # 'nedorogo':nedorogo
        }, content_type="application/xhtml+xml")

def seo(request, category, fil):

    for l in category:
        if l.isupper():
            return HttpResponsePermanentRedirect('/catalog/' + category.lower() + '/' + fil.lower() + '/')

    for l in fil:
        if l.isupper():
            return HttpResponsePermanentRedirect('/catalog/' + category.lower() + '/' + fil.lower() + '/')

    category = get_object_or_404(Category, slug=category)
    f = FilterSelect.objects.filter(slug=fil)
    f = f[0]
    fi = f.filter
    products = FilterItem.objects.filter(filter=fi, value=str(f.id)).values('product_id')
    items = Product.objects.filter(id__in=products, published = True)
    page = get_object_or_404(Seo, category=category, fil=f)
    try:
        compare_count = request.session['compare'][unicode(category.id)].index(request.session['compare'][unicode(category.id)][-1]) + 1
    except:
        compare_count = 0
    return render(request, 'shop/seo.html', {'items':items, 'page':page, 'category':category, 'compare_count': compare_count})

def seobrand(request, category, brand):

    return HttpResponsePermanentRedirect('/' + category + '/' + brand + '/')

    for l in category:
        if l.isupper():
            return HttpResponsePermanentRedirect('/category/' + category.lower() + '/' + brand.lower() + '/')

    for l in brand:
        if l.isupper():
            return HttpResponsePermanentRedirect('/category/' + category.lower() + '/' + brand.lower() + '/')

    category = get_object_or_404(Category, slug=category)
    brand = get_object_or_404(Brand, slug=brand)
    items = Product.objects.filter(category=category, brand=brand, published = True)
    page = SeoBrand.objects.filter(category=category, brand=brand)
    page = page[0]
    try:
        compare_count = request.session['compare'][unicode(category.id)].index(request.session['compare'][unicode(category.id)][-1]) + 1
    except:
        compare_count = 0
    return render(request, 'shop/seo_brand.html', {'items':items, 'page':page, 'brand':brand, 'category':category, 'compare_count': compare_count})

def poplyarnue(request, category):

    for l in category:
        if l.isupper():
            return HttpResponsePermanentRedirect('/poplyarnue/' + category.lower() + '/')

    category = get_object_or_404(Category, slug=category)
    page = Popular.objects.filter(category=category)
    page = page[0]
    items = Product.objects.filter(category=category, published = True).order_by('-count_views')[:30]
    try:
        compare_count = request.session['compare'][unicode(category.id)].index(request.session['compare'][unicode(category.id)][-1]) + 1
    except:
        compare_count = 0
    return render(request, 'shop/poplyarnue.html', {'items':items, 'page':page, 'category':category, 'compare_count': compare_count})

def nedorogo(request, category):

    for l in category:
        if l.isupper():
            return HttpResponsePermanentRedirect('/nedorogo/' + category.lower() + '/')

    category = get_object_or_404(Category, slug=category)
    page = LowPrice.objects.filter(category=category)
    page = page[0]
    items = Product.objects.filter(category=category, published = True).order_by('price')[:30]
    try:
        compare_count = request.session['compare'][unicode(category.id)].index(request.session['compare'][unicode(category.id)][-1]) + 1
    except:
        compare_count = 0
    return render(request, 'shop/nedorogo.html', {'items':items, 'page':page, 'category':category, 'compare_count': compare_count})


@never_cache
def hotline2(request):
    items = Product.objects.filter(published = True).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    for item in items:
        if item.price:
            row = []
            row.append(smart_unicode(item.category.name))
            row.append(smart_unicode(item.brand.name))
            row.append(smart_unicode(item.name)+" "+smart_unicode(item.maincolor))
            row.append(item.price)
            row.append(item.idname)
            row.append(u"http://20k.com.ua/"+item.category.slug+u"/"+item.brand.slug+u"/"+item.slug+u"/")
            row.append(u"http://20k.com.ua"+item.image.url)
            writer.writerow(row)
        if item.get_colors:
            for one in item.get_colors:
                if one['price']:
                    row = []
                    row.append(smart_unicode(item.category.name))
                    row.append(smart_unicode(item.brand.name))
                    row.append(smart_unicode(item.name)+" "+smart_unicode(one.name))
                    row.append(one['price'])
                    row.append(one['idname'])
                    row.append(u"http://20k.com.ua/"+item.category.slug+u"/"+item.brand.slug+u"/"+item.slug+u"/"+one['id']+u"/")
                    row.append(u"http://20k.com.ua/media/"+one['image1'])
                    writer.writerow(row)



    return response


@never_cache
def hotline(request):
    t = datetime.datetime.now()
    items = Product.objects.filter(Q(category__hotline=True) | Q(hotline=True), published = True).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/hotline.html', {'categorys':categorys, 't':t, 'c':c, 'items': items})

@never_cache
def nadavi(request):
    now = datetime.datetime.now()
    items = Product.objects.filter(Q(category__nadavi=True) | Q(nadavi=True), published = True, price__gt = 0).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/nadavi.html', {'categories':categorys, 'now':now, 'c':c, 'items': items}, content_type="application/xhtml+xml")

@never_cache
def priceua(request):
    t = datetime.datetime.now()
    items = Product.objects.filter(Q(category__priceua=True) | Q(priceua=True), published = True).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/hotline.html', {'categorys':categorys, 't':t, 'c':c, 'items': items})

@never_cache
def hotline_xml(request):
    t = datetime.datetime.now()
    items = Product.objects.filter(Q(category__hotline=True) | Q(hotline=True), published = True).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/hotline_xml.html', {'categorys':categorys, 't':t, 'c':c, 'items': items}, content_type="application/xhtml+xml")


@never_cache
def nadavi_xml(request):
    t = datetime.datetime.now()
    items = Product.objects.filter(Q(category__nadavi=True) | Q(nadavi=True), published = True, price__gt=0).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/hotline_xml.html', {'categorys':categorys, 't':t, 'c':c, 'items': items}, content_type="application/xhtml+xml")


@never_cache
def priceua_xml(request):
    t = datetime.datetime.now()
    items = Product.objects.filter(Q(category__priceua=True) | Q(priceua=True), published = True).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/priceua.html', {'categories':categorys, 'now':t, 'c':c, 'items': items}, content_type="application/xhtml+xml")



# def sitemap(request):
#     categorys = Category.objects.filter(published=1)
#     prods = Product.objects.filter(published=1)
#     return render(request, 'shop/google_sitemap.html', {"categorys":categorys, 'prods':prods}, content_type="application/xhtml+xml")
@never_cache
def yml(request):

    categories = Category.objects.filter(published = True)
    items = Product.objects.filter(published = True)

    return render(request, 'shop/yml.html', {
        'categories': categories,
        'items': items,
        'now' : datetime.datetime.now(),
        }, content_type="application/xhtml+xml")



def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def karta_sajta(request):
    categories = Category.objects.filter(published=1)
    return render(request, 'shop/sitemap.html',{'categories':categories})

def wwwwqqqq(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT * from shop_product2");
    res = dictfetchall(cursor)
    for i in res:
        try:
            p = Product.objects.get(pk=int(i['id']))
            p.price = i['price']
            p.save()
        except:
            pass
    return HttpResponse("ok")




@user_passes_test(lambda u: u.is_staff)
@never_cache
def get_filters_by_cat(request, id, product_id = False):
    results = []
    pfilters = []

    if product_id:
        pfilters = get_object_or_404(Product, pk=product_id).filters

    # assert False, pfilters
    category = Category.objects.get(pk=id)
    for item in category.filters.all():
        nitem = {'id': item.id, 'name': item.name, 'items': []}
        for fi in item.items:
            active = False
            if pfilters and fi.id in pfilters:
                active = True

            nitem['items'].append({
                'name': fi.value,
                'id': fi.id,
                'active': active,
             })

        results.append(nitem)

    return HttpResponse(json.dumps(results), content_type="application/json")

@user_passes_test(lambda u: u.is_staff)
@never_cache
def get_properties_by_cat(request, id, product_id = False):

    category = get_object_or_404(Category, pk = id)

    allproperties = {}

    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        # properties = PropertyProduct.objects.filter(product_id = product_id)
        if product.properties:
            for item in product.properties:
                allproperties[item[0]] = item[2]
    properties = category.properties.all()

    items = []

    for property in properties:
        if property.id in allproperties:
            value = allproperties[property.id]
        else:
            value = ''

        item = {
            'id': property.id,
            'name': property.name,
            'value': value,
        }
        items.append(item)

    data = json.dumps(items)

    return HttpResponse(data, content_type="application/json")

def prod_list(request):
    return render(request, 'shop/catalog.html', {})

def brand(request, slug):
    pass


# @never_cache
# def search(request):
#     q = unicode(request.GET.get('search', ''))
#     sq = q.replace(' ', '')

#     citems = []
#     if len(q)>2:

#         # assert False, q == u'Скидки'
#         if q == u'Акции':
#             items = Product.objects.filter(
#                 action=1, price__gt=0, published=1).order_by('?')
#         elif q == u'Скидки':
#             items = Product.objects.filter(
#                 oldprice__gt=0, price__gt=0, published=1).order_by('?')
#         else:
#             items = Product.objects.filter(
#                 Q(nameo__icntains = q) | Q(name__icontains = sq) | Q(idname__icontains = q) | Q(idname__icontains = sq), published = True).distinct()

#         items = items[:96]

#         if not len(items):

#             citems = ColorProduct.objects.filter(Q(idname__icontains = q) | Q(name__icontains = sq))

#             if len(citems):

#                 return redirect(citems[0].get_url())

#     else:
#         items = []

#     return render(request, 'shop/search.html', {'search': q, 'items': items, 'citems': citems})
@never_cache
def search(request, in_product = False):
    # assert False, in_product
    q = unicode(request.GET.get('search', ''))
    full_path_clean = '/search/?search=' + q
    # assert False, full_path_clean
    sq = q.replace(' ', '')
    if 'category[]' in request.GET:
        active_cats = request.GET.__getitem__('category[]')
        # for category in result_brands:
        #     active_brand = request.GET.get('brand_' + str(brand.id), 0)
        #     if active_brand:
        #         active_brands.append(brand)
    else:
        active_cats = []
    # assert False, Product.objects.filter(recomend = True)
    search_idname = []
    search_items = []
    parent_lists = []
    child_categories = []
    items = []
    import time

    categories = Category.objects.filter(level = 0, published = True)

    resulttime = {}

    # if q == u'Акции':
    #     search_items = Product.objects.filter(
    #         action=1, price__gt=0, published=1).order_by('-weight')
    # elif q == u'Скидки':
    #     search_items = Product.objects.filter(
    #         oldprice__gt=0, price__gt=0, published=1).order_by('-weight')

    # el
    if len(q)>2:

        # search_idname = Product.objects.filter(Q(idname__icontains = q) | Q(idname__icontains = sq), published = True).distinct().order_by('-weight')
        # search_items = Product.objects.filter(Q(name__icontains = q) | Q(name__icontains = sq) | Q(maincolor__icontains = q) | Q(maincolor__icontains = sq), published = True).distinct().order_by('-weight')


        items = search_items = Product.objects.filter(Q(name__icontains = q) | Q(name__icontains = sq) | Q(idname__icontains = q) | Q(idname__icontains = sq), published = True).distinct().order_by('-weight')
        if not items:
            items = search_items = Product.objects.filter(search__search=q, published=True)

        # compatibles = PartNumber.objects.filter(Q(name__icontains = q) | Q(name__icontains = sq))
        # similars = SimularModels.objects.filter(Q(name__icontains = q) | Q(name__icontains = sq))
        # items_similar = Product.objects.filter(Q(partnumber__in = compatibles) | Q(simularmodels__in = similars)).distinct()
        # assert False, search_items

        # items = items_similar | items
        # items = search_idname | search_items

        # assert False, items


        parent_lists = []
        # assert False, parent_lists
        newq = q.strip()
        newqlist = newq.split(' ')

        if len(newqlist) > 1:
            newitems = Product.objects

            for oneq in newqlist:
                if oneq:
                    newitems = newitems.filter(name__icontains = oneq)

            if newitems:
                items = newitems

        results = []
        search_cats = []


        category_id = request.GET.get('category_id', 0)

        if category_id:
            scat = Category.objects.filter(id = category_id)
            if scat:
                search_cats.append(int(category_id))
                for one in scat.get().get_children():
                    search_cats.append(one.id)


        source_cats = items.values('category').distinct()
        # assert False, source_cats

        active_cats = []
        for cat in source_cats:
            if request.GET.get('category_' + str(cat['category'])):
                active_cats.append(cat['category'])
            if cat['category'] in search_cats and not cat['category'] in active_cats:
                active_cats.append(cat['category'])

        child_categories = []

        if items:
            # t = time.time()
            child_categories = Category.objects.filter(product__in = items, published = True).distinct()
            # assert False, time.time() - t

            for child in child_categories:

                parent = child.parent

                if not parent in parent_lists:
                    parent_lists.append(parent)
                if not child.level and not child in parent_lists:
                    parent_lists.append(child)


                main_categoties =  Category.objects.filter(level = 0, published = True).distinct()
            # assert False, main_categoties

        if active_cats:
            items = items.filter(category_id__in=active_cats)

        # cont_items = items.count()
        if not len(items):

            citems = ColorProduct.objects.filter(Q(idname__icontains = q) | Q(name__icontains = sq))
            items = []

            for it in citems:
                items.append(it.product)




        # per_page_tuple = (15, 30, 60, 90, 'all')

        # per_page = request.session.get('per_page')
        # per_page_get = request.GET.get('per_page', 0)
        # if not per_page:
        #     per_page = 15

        # if per_page_get == 'all':
        #     per_page = 99999
        # elif per_page_get == 0:
        #     per_page = 15
        # else:
        #     per_page = per_page_get

        # if per_page_get not in per_page_tuple and per_page != 15:
        #     raise Http404

        # paginator = Paginator(items, per_page) # Show 25 contacts per page

        # if per_page_get == 'all':
        #     page = None
        # else:
        #     page = request.GET.get('page')

        # try:
        #     items = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer, deliver first page.
        #     items = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range (e.g. 9999), deliver last page of results.
        #     raise Http404
        #     # items = paginator.page(paginator.num_pages)

    else:
        items = []
        # return HttpResponse('empty')

    results_items = []
    results_items_not = []

    if search_idname:

        for one in search_idname:
            if one in items:
                if one.price > 0:
                    results_items.append(one)
                else:
                    results_items_not.append(one)

    if search_items:
        for one in search_items:
            if one in items:
                if one.price > 0:
                    results_items.append(one)
                else:
                    results_items_not.append(one)

    results_items += results_items_not

    cont_items = len(results_items)

    newcats = Category.objects.filter(id__in = active_cats)
    active_cats = []
    for one in newcats:
        if one.id not in active_cats:
            active_cats.append(one.id)

        if one.parent_id not in active_cats:
            active_cats.append(one.parent_id)


    newpath = '/search/?search=' + q

    for cat in active_cats:
        newpath += '&category_' + str(cat) +'=1'

    # assert False, active_cats


    if request.is_ajax():
        for item in results_items[:8]:
            if item.image2:
                rimg =  "/media/" + str(item.image)
            else:
                rimg = "/static_cdn/design/img/noimage.png" 

            results.append({'name': item.name, 'href': item.get_url, 'image': rimg, 'price': int(item.price)})
        data = json.dumps(results)

        return HttpResponse(data, content_type="application/json")

    if not results_items:

        search_idname = ColorProduct.objects.filter(Q(idname__icontains = q) | Q(idname__icontains = sq), product__published=True)
        # search_items = ColorProduct.objects.filter(Q(name__icontains = q) | Q(name__icontains = sq), published = True).distinct().order_by('-weight')
        if search_idname:
            return HttpResponsePermanentRedirect(search_idname[0].get_url())


    per_page = 96
    page = request.GET.get('page', 0)

    # assert False, results_items

    paginator = Paginator(results_items, per_page) # Show 25 contacts per page

    # assert False, page_brand
    if not page:
        page = None
    # page = request.GET.get('page')
    try:
        results_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # items = paginator.page(paginator.num_pages)
        raise Http404

    return render(request, 'shop/search.html', {
        'search': q,
        'items': results_items,
        'parent_lists': parent_lists,
        'child_categories': child_categories,
        'cont_items': cont_items,
        'active_cats': active_cats,
        'newpath': newpath,
        'full_path_clean': full_path_clean,
        })

@never_cache
def action(request, page=False):

    q = u'Акции'
    items = Product.objects.filter(
        action=1, price__gt=0, published=1).order_by('-weight')

    per_page = 96
    # page = request.GET.get('page', 0)

    paginator = Paginator(items, per_page) # Show 25 contacts per page

    # assert False, page_brand
    if not page:
        page = None
    # page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # items = paginator.page(paginator.num_pages)
        raise Http404


    return render(request, 'shop/action.html', {
        'search': q,
        'items': items,
        'category_url': '/action/'
        })





@never_cache
def top20(request):

    from django.utils.html import strip_tags
    from content.models import Snipet

    q = Snipet.objects.get(pk=3).text

    # q = u'Топ 20'
    items = Product.objects.filter(
        top20=True, published=1).order_by('-weight')

    return render(request, 'shop/action.html', {
        'search': q,
        'items': items,
        })


def discount(request, page=False):
    q = u'Скидки'
    items = Product.objects.filter(
        oldprice__gt=0, price__gt=0, published=1).order_by('-weight')

    per_page = 96
    # page = request.GET.get('page', 0)

    paginator = Paginator(items, per_page) # Show 25 contacts per page

    # assert False, page_brand
    if not page:
        page = None
    # page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # items = paginator.page(paginator.num_pages)
        raise Http404



    return render(request, 'shop/action.html', {
        'search': q,
        'items': items,
        'category_url': '/discount/'
    })


@never_cache
def category(request, slug):
    for l in slug:
        if l.isupper():
            get_full_path_list = request.get_full_path().split('?')
            if len(get_full_path_list) > 1:
                ending = '?' + get_full_path_list[1]
            else:
                ending = ''
            return HttpResponsePermanentRedirect('/' + slug.lower() + '/' + ending)

    # assert False, request.get_full_path()

    return get_category_data(request, slug)


def get_category_data(request, slug, category_brand = None, page_category = None, page_brand = None):
    # assert False, page_brand
    if page_category:
        page = page_category
    elif page_brand:
        page = page_brand
    else:
        page = None
    # assert False, page

    if page == 1:
        get_full_path_list = request.get_full_path().split('?')
        path = get_full_path_list[0].replace('page-1/', '')
        if len(get_full_path_list) > 1:
            ending = '?' + get_full_path_list[1]
        else:
            ending = ''
        # assert False, path + ending
        return HttpResponsePermanentRedirect(path + ending)

    per_page_tuple = (32, 64, 96,)

    order_by_tuple = (u'-id', u'name', u'-name', u'price', u'-price', u'count_views', u'-count_views')

# get category
    category = get_object_or_404(Category, slug = slug, published = True)

    if slug == 'remont':
        # assert False, slug
        page = {
            'title': category.title,
            'metaDesc': category.metadesc,
            'metaKey': category.metakey,
            'get_url': category.get_url(),
            'name': category.name,
            'full_text': category.text,
        }
        return render(request, 'content/page.html', {'page':page})

    child_categories = Category.objects.filter(parent=category)


    if child_categories:

        brands = Product.objects.filter(
            category__in=child_categories, published=True
        ).values('brand').distinct()
        # assert False, brands

        brand_ids_in = []
        for brand in brands:
            brand_ids_in.append(brand['brand'])

        result_brands = Brand.objects.filter(
            pk__in=brand_ids_in, published=True).order_by('name').distinct()
        categorys = None
        if '/amp/' in request.get_full_path():
            categorys = Category.objects.filter(published=True, parent=None).order_by('ordering')
            html='shop/catamp.html'
        else:
            html='shop/child-catalog.html'
        return render(request, html, {
            'category': category,
            'items': child_categories,
            'brands': result_brands,
            'ancor':Ancor.objects.filter(published=True),
            "categorys":categorys,
        })

    else:

        brands = Product.objects.filter(
            category=category, published=True).values('brand').distinct()
        brand_ids_in = []

        for brand in brands:
            brand_ids_in.append(brand['brand'])
        # assert False, brand_ids_in

        result_brands = Brand.objects.filter(pk__in = brand_ids_in, published = True).order_by('name').distinct()
        filters = list(category.filters.all().values())

        all_filters = []

        active_filters = []
        active_filters_list = []

        seofilter = False
    # get filter select

        products_args = {'category': category, 'published': True}

        active_brands = []

        seo_filters_categories = []

        if category_brand:

            seofilter = FilterSeo.objects.filter(slug=category_brand, category=category)
            # if seofilter:
            # assert False, seofilter
            if seofilter:
                seofilter = seofilter[0]

                if seofilter.brand:
                    active_brands.append(seofilter.brand_id)

                if seofilter.fs1:
                    seo_filters_categories.append(seofilter.fs1_id)

                if seofilter.fs2:
                    seo_filters_categories.append(seofilter.fs2_id)

                if seofilter.fs3:
                    seo_filters_categories.append(seofilter.fs3_id)

            else:
                raise Http404


        else:
            category_brand = None

            for brand in result_brands:
                active_brand = request.GET.get('brand_' + str(brand.id), 0)
                if active_brand:
                    # assert False, brand.id
                    active_brands.append(brand.id)
        # assert False, category_brand

        if active_brands:
            products_args['brand__in'] = active_brands

        filteritems = {}
        fi = 0

        filteritems = {}

        allfiltersnew = {}

        for filter in filters:
            fi += 1
            items = FilterSelect.objects.filter(filter_id = filter['id']).order_by('ordering')
            filter['items'] = items
            all_filters.append(filter)
            filteritems[fi] = []



            for item in items:
                name = 'prop_' + str(item.id)
                filter_prop = request.GET.get(name, 0)
                if filter_prop or item.id in seo_filters_categories:
                    one_active_filter = {'filter_id': filter['id'], 'value': str(item.id)}
                    active_filters.append(one_active_filter)
                    active_filters_list.append(item.id)
                    filteritems[fi].append(one_active_filter)

                    if item.filter.pk in allfiltersnew:
                        allfiltersnew[item.filter.pk].append(item.id)
                    else:
                        allfiltersnew[item.filter.pk] = [item.id]

        all_filters = sorted(all_filters, key=lambda k: k['ordering'])
        results_products_set = set([])

        allq = []
        qfinal = False

        # assert False, active_filters_listist
        # if len(allfiltersnew):
        #     products_args['filters__contains'] = []
        #     allq = []


        for findex, fvalues in allfiltersnew.iteritems():
            if len(fvalues) > 1:

                queries = [Q(filters__contains=value) for value in fvalues]

                query = queries.pop()

                for item in queries:
                    query |= item

                allq.append((query))



            else:
                if 'filters__contains' in products_args:
                    products_args['filters__contains'].append(fvalues[0])
                else:
                    products_args['filters__contains'] = [fvalues[0]]

            # pass
        # assert False, allq

        if len(allq)>1:
            qfinal = allq.pop()

            for oneq in allq:
                qfinal &= oneq

        elif len(allq)==1:
            qfinal = allq.pop()


        # assert False, allfiltersnew
        # assert False, active_filters
        # assert False, filteritems

        # if active_filters:
        #     for activef in filteritems:

        #         if len(filteritems[activef]):

        #             temp_product_set = False

        #             for onef in filteritems[activef]:


        #                 products_list = []

        #                 products = FilterItem.objects.filter(**onef).values('product_id')

        #                 for one in products:
        #                     products_list.append(one['product_id'])

        #                 products_set = set(products_list)
        #                 if temp_product_set:
        #                     temp_product_set = temp_product_set | products_set
        #                 else:
        #                     temp_product_set = products_set

        #             if results_products_set:

        #                 results_products_set = results_products_set & temp_product_set

        #             else:

        #                 results_products_set = temp_product_set

        #     # assert False, results_products_set

        #     products_ids = list(results_products_set)

        #     products_args['pk__in'] = products_ids
        # assert False, products_args

        # if active_filters:
        #     searchfilters = []
        #     for af in active_filters:
        #         searchfilters.append(int(af['value']))

        #     products_args['filters__contains'] = searchfilters


        if len(active_brands) <= 1 and not category_brand:

            key = ""

            if active_brands:
                brand = Brand.objects.filter(pk = active_brands[0])[0]
                key += "brand_" + str(brand.id)

            if active_filters:
                for onefil in active_filters:
                    key += "prop_" + str(onefil['value'])

            # assert False, active_filters

            if key and key in category.getseo:

                return HttpResponsePermanentRedirect('/' + category.slug.lower() + '/' + category.getseo[key] + '/')


        order_by = request.session.get('order_by')

        order_by_get = request.GET.get('order_by', '')

        if not order_by:
            order_by = '-id'

        if order_by_get in order_by_tuple:
            # assert False, per_page_get
            request.session['order_by'] = order_by_get
            order_by = order_by_get

        if order_by_get:

            return HttpResponsePermanentRedirect(request.get_full_path().split('?')[0])



        if qfinal:
           items = Product.objects.filter(qfinal,**products_args).order_by(order_by)
        else:
           items = Product.objects.filter(**products_args).order_by(order_by)

        if not items:
            not_items = True
            if category_brand:
                items = Product.objects.filter(category=category, published=True).order_by('?')
            elif active_filters:
                items = Product.objects.filter(category=category, published=True).order_by('?')
            elif category.parent:
                items = Product.objects.filter(
                    category__in=category.parent.get_children()).order_by('?')
        else:
            not_items = False
        # assert False, not_items
        if items:
            # assert False, items
            items_not_available = items.filter(price=0)
        else:
            items_not_available = []

        if items:
            items = items.filter(price__gt=0)

        if items:
            max_price = str(items.order_by('-price')[0].price).replace(',', '.')
            min_price = str(items.order_by('price')[0].price).replace(',', '.')

            if min_price == 'None':
                min_price = 0

        else:
            max_price = 0
            min_price = 0

        try:
            min_now = int(request.GET.get('min_now', 0))
        except:
            min_now = 0

        try:
            max_now = int(request.GET.get('max_now', 0))
        except:
            max_now = 0

        if max_now:
            items = items.filter(price__lte=max_now)

        if min_now:
            items = items.filter(price__gte=min_now)

        per_page = request.session.get('per_page')

        per_page_get = int(request.GET.get('per_page', 0))

        if not per_page:
            per_page = 32

        if per_page_get in per_page_tuple:
            # assert False, per_page_get
            request.session['per_page'] = per_page_get
            per_page = per_page_get

        if per_page_get:
            return HttpResponsePermanentRedirect(request.get_full_path().split('?')[0])

        citems = []

        for item in items:
            citems.append(item)

        for item in items_not_available:
            citems.append(item)
        items = citems

        if not_items:
            items = items[:32]
        # assert False, len(items)

        if not active_brands and not active_filters_list:
            paginator = Paginator(items, per_page) # Show 25 contacts per page

            # assert False, page_brand
            if not page:
                page = None
            # page = request.GET.get('page')
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                items = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                # items = paginator.page(paginator.num_pages)
                raise Http404

        if request.GET.get('page'):
            return HttpResponsePermanentRedirect(request.get_full_path().split('?')[0])


        get_full_path_list = request.get_full_path().split('?')
        # assert False, page

        if len(get_full_path_list) > 1:

            get_full_path = get_full_path_list[1]
            for one in order_by_tuple:
                get_full_path = get_full_path.replace(u'&order_by=' + one, '')
                get_full_path = get_full_path.replace(u'order_by=' + one, '')
            for one in per_page_tuple:
                get_full_path = get_full_path.replace(u'&per_page=' + str(one), '')
                get_full_path = get_full_path.replace(u'per_page=' + str(one), '')

        else:
            get_full_path = None



        # result = []

        # for item in result_brands:
        #     one = { 'id': item.id, 'brand': item, 'products': item.products(product.category)}
        #     result.append(one)


        try:
            compare_count = request.session['compare'][unicode(category.id)].index(request.session['compare'][unicode(category.id)][-1]) + 1
        except:
            compare_count = 0

        try:
            low_price = LowPrice.objects.get(category=category)
        except:
            low_price = ""
        try:
            popular = Popular.objects.get(category=category)
        except:
            popular = ""

        seo_brands = SeoBrand.objects.filter(category=category)
        # assert False, category_brand
        if not category_brand:
            html = 'shop/catalog.html'
            brand_description = None
            brand_url = None
        else:
            html = 'shop/brandcategory.html'
            try:
                brand_description = get_object_or_404(SeoBrand, category = category, brand = category_brand).full_text
            except:
                brand_description = None
            brand_url = '/' + str(category.slug) + '/' + str(category_brand) + '/'
            # assert False, brand_description
        # assert False, brand_url
        show_text = False
        if not active_brands and not active_filters and (page == None or page == 1):
            show_text = True
        
        categorys = None
        if '/amp/' in request.get_full_path():
            html = 'shop/catprodamp.html'
            categorys = Category.objects.filter(published=True, parent=None).order_by('ordering')
        return render(request, html, {
            'ancor':Ancor.objects.filter(published=True),
            'category': category,
            'brand': category_brand,
            'brand_description': brand_description,
            'brand_url': brand_url,
            'filters': all_filters,
            'items': items,
            'not_items': not_items,
            'page': page,
            'per_page': per_page,
            'per_page_tuple': per_page_tuple,
            'active_filters': active_filters_list,
            'get_full_path': get_full_path,
            'order_by': order_by,
            'active_brands': active_brands,
            'brands': result_brands,
            'max_price': max_price,
            'min_price': min_price,
            'max_now': max_now,
            'min_now': min_now,
            'compare_count': compare_count,
            'low_price':low_price,
            'popular':popular,
            'seo_brands':seo_brands,
            'seofilter' : seofilter,
            'show_text' : show_text,
            'categorys': categorys,
            })

def brandcategory(request, brand, category):
    for l in category:
        if l.isupper():
            get_full_path_list = request.get_full_path().split('?')
            # path = get_full_path_list[0].replace('page-1/', '')
            if len(get_full_path_list) > 1:
                ending = '?' + get_full_path_list[1]
            else:
                ending = ''
            return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/' + ending)

    for l in brand:
        if l.isupper():
            get_full_path_list = request.get_full_path().split('?')
            # path = get_full_path_list[0].replace('page-1/', '')
            if len(get_full_path_list) > 1:
                ending = '?' + get_full_path_list[1]
            else:
                ending = ''
            return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/' + ending)

    # assert False, request.get_full_path()
    if 'page-' in brand:
        # assert False, int(brand.split('page-')[1])
        page_category = int(brand.split('page-')[1])
        brand = None
        return get_category_data(request, category, brand, page_category)
    else:
        # page_category = None
        return get_category_data(request, category, brand)


    # brand = get_object_or_404(Brand, slug = brand, published = True)
    # category = get_object_or_404(Category, slug = category, published = True)
    # items = Product.objects.filter(brand = brand, category = category, published = True)
    # try:
    #     brand_description = get_object_or_404(BrandDescription, category = category, brand = brand)
    # except:
    #     brand_description = 0
    # # assert False, brand_description

    # try:
    #     compare_count = request.session['compare'][unicode(category.id)].index(request.session['compare'][unicode(category.id)][-1]) + 1
    # except:
    #     compare_count = 0

    # try:
    #     low_price = LowPrice.objects.get(category=category)
    # except:
    #     low_price = ""
    # try:
    #     popular = Popular.objects.get(category=category)
    # except:
    #     popular = ""

    # seo_brands = SeoBrand.objects.filter(category=category)

    # return render(request, 'shop/brandcategory.html', {
    #     'brand': brand,
    #     'category': category,
    #     'items': items,
    #     'compare_count': compare_count,
    #     'low_price':low_price,
    #     'popular':popular,
    #     'seo_brands':seo_brands,
    #     'brand_description':brand_description,
    #     })
def update_date(list):
    return [list[i:i+2] for i in range(0, len(list), 2)]

@cache_page(60 * 60 * 24)
def product(request, category, brand, product_slug, color_slug = False):

    # assert False, request.META['HTTP_REFERER']

    for l in category:
        if l.isupper():
            get_full_path_list = request.get_full_path().split('?')
            # path = get_full_path_list[0].replace('page-1/', '')
            if len(get_full_path_list) > 1:
                ending = '?' + get_full_path_list[1]
            else:
                ending = ''
            return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/' + product_slug.lower() + '/' + ending)

    for l in brand:
        if l.isupper():
            get_full_path_list = request.get_full_path().split('?')
            # path = get_full_path_list[0].replace('page-1/', '')
            if len(get_full_path_list) > 1:
                ending = '?' + get_full_path_list[1]
            else:
                ending = ''
            return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/' + product_slug.lower() + '/' + ending)

    for l in product_slug:
        if l.isupper():
            get_full_path_list = request.get_full_path().split('?')
            # path = get_full_path_list[0].replace('page-1/', '')
            if len(get_full_path_list) > 1:
                ending = '?' + get_full_path_list[1]
            else:
                ending = ''
            return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/' + product_slug.lower() + '/' + ending)

    # for l in product_slug:
    #     if l.isupper():
    #         get_full_path_list = request.get_full_path().split('?')
    #         # path = get_full_path_list[0].replace('page-1/', '')
    #         if len(get_full_path_list) > 1:
    #             ending = '?' + get_full_path_list[1]
    #         else:
    #             ending = ''
    #         return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/' + product_slug.lower() + '/' + ending)

    if 'page-' in product_slug:
        # assert False, int(brand.split('page-')[1])
        # page_category = None
        return HttpResponsePermanentRedirect('/' + category.lower() + '/' + brand.lower() + '/')

        # page_brand = int(product_slug.split('page-')[1])
        # return get_category_data(request, category, brand, page_brand = page_brand)

    product = get_object_or_404(Product, slug = product_slug, published = True)
    if 'HTTP_REFERER' in request.META and 'search/?search' in request.META['HTTP_REFERER']:
        product.weight +=1
        product.save()


    # product.idname = int(product.idname)

    filters = FilterItem.objects.filter(product=product)
    fils = []
    for f in filters:
        fils.append(int(f.value))

    # productprop = product.get_properties

    ip = get_client_ip(request)

    # product_viewed = ProductViews.objects.filter(product = product, ip_address = ip, date = datetime.date.today())

    # if not product_viewed:
    #     pviews = ProductViews(product = product, ip_address = ip)
    #     pviews.save()
    #     product.count_views+=1
    #     product.save()

    # assert False, product_viewed
    #
    if product.price:
        max_price = product.price + product.price / 10
        min_price = product.price - product.price / 10
    else:
        max_price = 0
        min_price = 0



    simular = Product.objects.filter(price__gt = min_price, price__lt = max_price, category = product.category, published = True).exclude(pk = product.id).order_by('?')[:4]

    # assert False, simular

    category = get_object_or_404(Category, slug = category)

    brand = get_object_or_404(Brand, slug = brand)

    photos = Photo.objects.filter(product = product)

    colors = ColorProduct.objects.filter(product = product)


    extras = list(product.extraproduct.all().filter(published = True, price__gt = 0))

    extrascategories = ExtraCategory.objects.filter(product_from = product)
    for one in extrascategories:
        newextra = list(Product.objects.filter(published = True, category = one.categort_to, price__gt = 0).exclude(pk = product.id).order_by('?')[:one.count])
        extras += newextra
    # assert False, extrascategories

    import random
    random.shuffle(extras,random.random)
    # assert False, extras
    if color_slug:

        for color in product.get_colors:
            if int(color_slug) == color['id']:
                photos = []
                product.image1 = product.image
                product.image = color['image1']
                product.name += " " + color['name']
                product.price = color['price']
                product.idname = color['idname']
                product.color_id = color['id']
                product.is_color = True

                # assert False, product.idname

                for i in range (2, 5):
                    if color['image' + str(i)]:
                        one = {
                            'name': product.name + ' ' + color['name'],
                            'image': color['image' + str(i)]
                        }
                        photos.append(one)
        color_complects = []
        color_complectitems = ComplectItem.objects.filter(product_id=color_slug)
        for complectitem in color_complectitems:
            if complectitem.complect.active:
                color_complects.append(complectitem.complect)
        # assert False, color_complects
    else:

        product.name += " " + product.maincolor
        product.image1 = product.image
        product.is_color = False

        # color_complectitems = None
        # color_complects = None
        color_complects = []

        complectargs = {'product_id': product.maincolor_id}

        if color_slug:
            complectargs = {'product_id': int(color_slug)}

        color_complectitems = ComplectItem.objects.filter(**complectargs)
        for complectitem in color_complectitems:
            if complectitem.complect.active:
                color_complects.append(complectitem.complect)
    # assert False, color_complects[0].items

    gifts = product.giftproduct.all().filter(published = True)
    # assert False, product.complects[0].items

    seo_pages = Seo.objects.filter(category=category, fil_id__in=fils)
    try:
        seo_brand = get_object_or_404(SeoBrand, category=category, brand=product.brand)
    except:
        seo_brand = ''

    from datetime import date

    today = date.today()

    # date_action = date(product.action_time.year, product.action_time.month,  product.action_time.day)
    # assert False, date_action
    from django.utils import timezone
    now = timezone.now()


    if product.action_time and now >= product.action_time:
        is_action = False
    else:
        is_action = True
    html = 'shop/product.html'
    categorys=None
    sim = None
    if '/amp/' in request.get_full_path():
        html = 'shop/prodamp.html'
        categorys = Category.objects.filter(published=True, parent=None).order_by('ordering')
        sim = update_date(Product.objects.filter(
        category=product.category, published=1, price__gt=0).order_by('?')[:12])
    # assert False, color_slug
    return render(request, html, {
        'category': category,
        'brand': brand,
        'product': product,
        'photos': photos,
        'colors': colors,
        'simular': simular,
        'extras': extras,
        'color_slug': int(color_slug),
        'color_complectitems': color_complectitems,
        'color_complects': color_complects,
        'gifts': gifts,
        # 'productprop': productprop,
        'now': datetime.datetime.now(),
        'fils':fils,
        'seo_pages':seo_pages,
        'seo_brand':seo_brand,
        'is_action':is_action,
        'ancor':Ancor.objects.filter(published=True),
        'categorys':categorys,
        'sim':sim,
    })

def add_to_session(request, product_id, type_cart):

    if type_cart in request.session:
        if str(product_id) in request.session[type_cart].keys():
            request.session[type_cart][str(product_id)] += 1
        else:
            request.session[type_cart][str(product_id)] = 1

    else:
        request.session[type_cart] = {}
        request.session[type_cart] = {str(product_id): 1}

    return show_cart(request)

@never_cache
def add_to_cart(request, id, color = False):


    request.session.modified = True

    # assert False, id
    if color:

        color = get_object_or_404(ColorProduct, pk = int(color))

        product_id = str(color.product.id) + '_' + str(color.id)

    else:

        product_id = int(id)

        get_object_or_404(Product, pk = product_id, published = True)


    # assert False,
    # request.session.modified = True
    return add_to_session(request, product_id, 'cart')

@never_cache
def add_to_cart_one(request, id, color = False):


    request.session.modified = True

    # assert False, id
    try:

        color = get_object_or_404(ColorProduct, pk = int(color))

        product_id = str(color.product.id) + '_' + str(color.id)

    except:

        product_id = int(id)

        get_object_or_404(Product, pk = product_id, published = True)


    # assert False,
    # request.session.modified = True
    add_to_session(request, product_id, 'cart')
    return HttpResponsePermanentRedirect('/checkout/step1/')
    # assert False, request.session['cart']
# @never_cache
def add_complect(request, id, color = False):


    request.session.modified = True

    complect = get_object_or_404(Complect, pk = int(id))

    # assert False, id
    if color:

        color = get_object_or_404(ColorProduct, pk = int(color))

        # product_id = str(complect.id) + '_' + str(color.id)
        product_id = str(complect.id)

    else:

        product_id = int(id)

        # get_object_or_404(Product, pk = product_id, published = True)


    # assert False, product_id
    # request.session.modified = True
    return add_to_session(request, product_id, 'complect')

    # assert False, request.session['cart']

# @never_cache
def show_cart(request):
    # assert False, request.session['complect']
    # request.session['complect'] = {}
    result = get_cart_data(request)

    request.session['allcount'] = result['allcount']
    request.session['allprice'] = result['allprice']

    # assert False, result
    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")

def get_cart_data(request):

    colors_in = []
    products_in = []
    complect_in = []
    complect_colors_in = {}

    if 'cart' in request.session:
        for item in request.session['cart'].keys():
            if '_' in item:
                colors_in.append(int(item.split('_')[1]))
            else:
                products_in.append(int(item))

    if 'complect' in request.session:
        for item in request.session['complect'].keys():
            if '_' in item:
                complect_colors_in[int(item.split('_')[0])] = item
                complect_in.append(int(item.split('_')[0]))
            else:
                complect_in.append(int(item))
    # assert False, complect_in

    pitems = Product.objects.filter(pk__in = products_in, published = True)
    citems = ColorProduct.objects.filter(pk__in = colors_in)
    complects = Complect.objects.filter(pk__in = complect_in)

    # assert False, citems

    allitems = []
    allcomplects = []

    allprice = 0
    allcount = 0

    result = {}

    for item in pitems:
        count = int(request.session['cart'][str(item.id)])
        price = float(item.price)

        one = {
            'link'  : item.get_url,
            'name'  : item.name,
            'idname'  : item.idname,
            'category'  : item.category.name,
            'count' : count,
            'image' : str(item.small_image),
            'id'    : item.id,
            'price' : price
        }

        allcount += count
        allprice += count * price
        allitems.append(one)

    for item in citems:

        item_id = str(item.product.id) + '_'+ str(item.id)

        count = int(request.session['cart'][item_id])
        price = float(item.price)

        one = {
            'link'  : item.get_url(),
            'name'  : item.get_name,
            'idname'  : item.idname,
            'category'  : item.product.category.name,
            'count' : count,
            'image' : str(item.small_image),
            'id'    : item_id,
            'price' : price
        }
        # assert False, one

        allcount += count
        allprice += count * price
        allitems.append(one)

    for item in complects:
        if item.id in complect_colors_in.keys():
            count = int(request.session['complect'][str(complect_colors_in[item.id])])
            # assert False, count
        else:
            count = int(request.session['complect'][str(item.id)])
        # assert False, count
        price = float(item.price)

        one = {
            # 'link'  : item.get_url(),
            'name'  : item.name,
            'count' : count,
            # 'image' : str(item.small_image),
            'id'    : item.id,
            'price' : int(price),
            'items' : [],
            'total' : int(count * price)
        }


# a = '123' if b else '456'
        for product in item.items:
            one['items'].append({
                'link'  : product.product.get_url(),
                'name'  : product.product.product.name,
                'image' : str(product.product.small_image),
                'percent': product.percent,
                'oldprice':  int(product.product.price if product.price else  0),
                'price': int(product.price if product.price else product.product.price),
            })
            # assert False, product.product.product.name


        allcount += count
        allprice += count * price
        allcomplects.append(one)



    result = {
        'items'     : allitems,
        'allcount'  : allcount,
        'allprice'  : allprice,
        'complects' : allcomplects,
    }
    # assert False, allcount
    return result


@never_cache
def change_cart(request):
    if 'cart' in request.session:
        for one in request.session['cart'].keys():
            quant = int(request.POST.get('quantity_' + str(one), 1))
            if quant > 0:
                request.session['cart'][str(one)] = quant
            else:
                del request.session['cart'][str(one)]
    if 'complect' in request.session:
        for one in request.session['complect'].keys():
            quant = int(request.POST.get('complect_' + str(one), 1))
            if quant > 0:
                request.session['complect'][str(one)] = quant
                # assert False, request.session['complect'][str(one)]
            else:
                del request.session['complect'][str(one)]
    return show_cart(request)
@never_cache
def step1(request):
    from .forms import *

    if 'cart' not  in request.session and 'complect' not in request.session:
        return render(request, 'shop/emptycart.html', {})

    result = get_cart_data(request)

    # assert False, result['complects']




    if request.method == 'POST':
        form = OrderForm(request.user, request.POST)
        if form.is_valid():
            order = form.save()
            email = form.cleaned_data['email']
            if email:
                try:
                    u = User.objects.get(email=email)
                except:
                    u = User.objects.create_user(email=email, username=email, password='12345')
                    u.first_name = form.cleaned_data['name']
                    u.phone = form.cleaned_data['phone']
                    u.save()


            if request.user.is_authenticated():
                request.user.first_name = form.cleaned_data['name']
                # request.user.email = request.POST.get('email')
                request.user.last_name = form.cleaned_data['lastname']
                request.user.phone = form.cleaned_data['phone']

                request.user.save()
                order.user = request.user

            if form.cleaned_data['delivery'] == 2:
                delivery_address = request.POST.get('delivery_address', '')
                place = OrderPlace(order = order, place = delivery_address)
                place.save()

            if form.cleaned_data['delivery'] == 3:
                deliveryservice = request.POST.get('delivery_service', '')
                place = OrderDelivery(order = order, deliveryservice = deliveryservice)
                place.save()

            order.pub_date = datetime.datetime.now()
            order.save()

            # assert False, order

            colors_in = []
            products_in = []
            complect_in = []
            complect_color_in = []

            if "cart" in request.session:
                for item in request.session['cart'].keys():
                    if '_' in item:
                        colors_in.append(int(item.split('_')[1]))
                    else:
                        products_in.append(int(item))


            if 'complect' in request.session:
                for item in request.session['complect'].keys():
                    if '_' in item:
                        complect_in.append(int(item.split('_')[1]))
                    else:
                        complect_in.append(int(item))

            for one in products_in:
                # try:

                product = Product.objects.filter(pk = int(one)).get()
                orderproduct = OrderProduct(order = order, product = product, price = product.price, count = request.session['cart'][str(one)])
                orderproduct.save()
                # except e:
                #     assert False, one

            for one in colors_in:
                color = ColorProduct.objects.filter(pk = int(one)).get()
                color_id = str(color.product.id) + '_'+ str(color.id)

                # assert False, color.price

                ordercolor = OrderColor(order = order, color = color, price = color.price, count = request.session['cart'][color_id])
                ordercolor.save()

            for one in complect_in:
                # try:
                complect = Complect.objects.filter(pk = one).get()
                ordercomplect = OrderComplect(order = order, complect = complect, price = complect.price, count = request.session['complect'][str(one)] )
                ordercomplect.save()

                # except e:
                    # assert False, e


            if 'cart' in request.session:
                del request.session['cart']

            if 'complect' in request.session:
                del request.session['complect']

            request.session['allcount'] = 0
            request.session['allprice'] = 0
            return redirect("/checkout/thanx/")
            # assert False, result['complects'][0]['name']
            # return render(request, 'shop/confirm.html', {'result': result, 'form': form, 'order': order})
        else:

            if request.user.is_authenticated():
                render_script = 'shop/step1.html'
            else:
                render_script = 'shop/step1.html'
                # assert False, get_full_path()

            return redirect("/checkout/thanx/")
            # return render(request, render_script, {'result': result, 'form': form })

    if request.user.is_authenticated():

        initialdata = {
            'name': request.user.first_name,
            'phone': request.user.phone,
            'email': request.user.email,
        }

        form = OrderForm(request.user, initial = initialdata)
        # assert False, request.get_full_path()

        return render(request, 'shop/step1.html', {'result': result, 'form': form })



    form = OrderForm(request.user)


    return render(request, 'shop/step1.html', {'result': result, 'form': form})

def step2(request):

    return render(request, 'shop/step2.html', {})


def thanx(request):

    return render(request, 'shop/thanx.html', {})

def get_price(price):
    if price:
        price = price.replace('\n', '').replace('\t', '').replace(',', '.')
        price = float(price)
    else:
        price = 0

    return price

def export(request):

    def httpauth():
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm=""'
        return response

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            # NOTE: We are only support basic authentication for now.
            #
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None or True:
                    # if user.is_active or True:
                        # login(request, user)
                        # request.user = user

                        from lxml import etree


                        parser = etree.XMLParser(recover=True)
                        body = etree.fromstring(request.body, parser)

                        items = body.xpath('//product')

                        all = 0
                        news = 0
                        edited = 0
                        for item in items:
                            all += 1
                            idname = item.xpath('.//id')[0].text.replace('\n', '').replace('\t', '')

                            try:
                                category = item.xpath('.//model')[0].text.replace('\n', '').replace('\t', '')
                            except:
                                category = None

                            try:
                                brand = item.xpath('.//brand')[0].text.replace('\n', '').replace('\t', '')
                            except:
                                brand = None

                            try:
                                model = item.xpath('.//name')[0].text.replace('\n', '').replace('\t', '')
                            except :
                                model = None

                            try:
                                price = item.xpath('.//price')[0].text
                                price = get_price(price)
                            except:
                                price = 0


                            try:
                                price_incoming = item.xpath('.//price_incoming')[0].text
                                price_incoming = get_price(price_incoming)

                            except:
                                price_incoming = 0

                            # product = Product.objects.filter(idname = idname)
                            color = ColorProduct.objects.filter(idname = idname)

                            # if product.exists():
                            #     product = product[0]
                            #     product.price = price
                            #     product.save()
                            #     edited += 1



                            if color.exists():
                                try:
                                    product = color[0]
                                    product.price_in = price_incoming
                                    product.price = price
                                    product.save()
                                    edited += 1
                                except Exception, e:
                                    send_mail('Export error', product.name, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)

                                    pass
                            else:

                                if not category:

                                    pcategory = None

                                else:

                                    pcategory = Category.objects.filter(name = category)

                                    if pcategory.exists():
                                        pcategory = pcategory.get()

                                    else:

                                        pcategory = Category(name = category, published = False, slug = makeslugify(category, 'Category'))
                                        pcategory = pcategory.save()

                                if not brand:

                                    pbrand = None

                                else:

                                    pbrand = Brand.objects.filter(name = brand)

                                    if pbrand.exists():
                                        pbrand = pbrand.get()

                                    else:

                                        pbrand = Brand(name = brand, published = False, slug = makeslugify(brand, 'Brand'))
                                        pbrand = pbrand.save()
                                if model:
                                    try:
                                        product = Product(
                                            name = model,
                                            price = price,
                                            # name = model,
                                            category = pcategory,
                                            brand = pbrand,
                                            published = False,
                                            is_new = True,
                                            slug = makeslugify(model, 'Product'),
                                            idname = idname,
                                        )

                                        news += 1

                                        product.save()
                                    except:
                                        pass

                                    try:
                                        color = ColorProduct(
                                            name = model,
                                            price = price,
                                            idname = idname,
                                            product = product,
                                            )
                                        color.save()
                                    except Exception, e:
                                        pass
                                        # raisee e
                        send_mail('Export', request.body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)

                        items = ComplectItem.objects.all()

                        for item in items:
                            item.save()

                        colors = ColorProduct.objects.filter(product__price = 0, price__gt=0, main=False)
                        products = []

                        for color in colors:

                            color.main = True
                            color.save()

                            products.append(color.product)


                        oldcolors = ColorProduct.objects.filter(price = 0, main = True, product__in = products)
                        for old in oldcolors:

                            old.main = False

                            old.save()


                        from grab import Grab
                        g = Grab(timeout=300)
                        g.go('http://20kold.gowius.com/export/', post=request.body, userpwd="mozger@ukr.net:ilove20k")



                        return HttpResponse('Загружено: ' + str(all) + ' из '+ str(all) + '. Из них новых: ' + str(news) )
        return httpauth()
        # return HttpResponse('Authorization failed')

    return httpauth()
    # Either they did not provide an authorization header or
    # something in the authorization attempt failed. Send a 401
    # back to them to ask them to authenticate.



def export_orders(request):

    def httpauth():
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm=""'
        return response

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            # NOTE: We are only support basic authentication for now.
            #
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        send_mail('Export', request.body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)

                        return HttpResponse('Загружено все заказы')
        return httpauth()
        # return HttpResponse('Authorization failed')

    return httpauth()
    # Either they did not provide an authorization header or
    # something in the authorization attempt failed. Send a 401
    # back to them to ask them to authenticate.


def makeslugify(name, modelname):
    from slugify import slugify
    slug = slugify(name)

    namedclass = {'Product': Product, 'Brand': Brand, 'Category': Category}

    if namedclass[modelname].objects.filter(slug = slug).exists():
        slug += str(random.randint(0, 10000000))

    return slug


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def google_feed(request):
    t = datetime.datetime.now()
    items = Product.objects.filter(published = True, price__gt=1).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')
    c = items.count()
    categorys = Category.objects.filter(published=1)
    return render(request, 'shop/feed.html', {'categorys':categorys, 't':t, 'c':c, 'items': items})


@never_cache
def clear_compare(request):
    # assert False,  request.session['compare']
    # request.session.modified = True
    # request.session['compare'].clear()
    pass


@never_cache
def compare_list(request):
    # assert False,  request.session['compare']
    result = []
    for item in request.session['compare'].keys():
        category_name = Category.objects.filter(id=item)[0].name
        qt_product = len(request.session['compare'][item])

        one = {
            'id': item,
            'name': category_name,
            'qt': qt_product,
        }
        result.append(one)

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")


@never_cache
def compare(request):
    item_id = int(request.POST.get('id', 0))

    # assert False, item_id

    # result = {}
    if 'compare' not in request.session:
        result = {}
    else:
        result = request.session['compare']

    if item_id:

        category = get_object_or_404(Category, product__id = item_id, published = True)
        # assert False, request.session['compare']
        cat_id = str(category.id)

        # assert False, category.id not in request.session['compare']
        if cat_id not in result:
            result[cat_id] = []
        # request.session.compare = [category.id = [1]]

        if item_id not in result[cat_id]:
            result[cat_id].append(item_id)
        else:
            result[cat_id].remove(item_id)


    request.session['compare']= result

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")


@never_cache
def to_compare(request, category_id):

    if request.method == 'POST':
        item_id = int(request.POST.get('item_id'))
        result = request.session['compare']
        result[category_id].remove(item_id)
        request.session['compare'] = result
        count_id = request.session['compare'][category_id].index(request.session['compare'][category_id][-1]) + 1
        return HttpResponse(count_id)

    # assert False, request.session['compare'][category_id]

    category = get_object_or_404(Category, pk = category_id)

    try:
        prods_id = request.session['compare'][category_id]
    except:
        prods_id = []

    prods = Product.objects.filter(pk__in = prods_id, published = True)

    properties = Property.objects.filter(category = category)
    properties_id = []
    for p in properties:
        properties_id.append(int(p.id))


    prod_properties = PropertyProduct.objects.filter(product__in = prods, property__in = properties)
    # assert False, prod_properties.count()

    return render(request, 'shop/compare.html', {
        'category':category,
        'prods':prods,
        'prods_id':prods_id,
        'properties':properties,
        'properties_id':properties_id,
        'prod_properties':prod_properties,
    })


@never_cache
def oneclick(request):
    phone = str(request.POST['phone'])
    product_id = int(request.POST['product_id'])

    product = get_object_or_404(Product, id = product_id)

    quikorder = QuikOrder(product = product, phone = phone, pub_date = datetime.datetime.now(), producttext=product.name + ": " + str(product.price))
    quikorder.save()

    # msg = EmailMessage('Покупка в 1 клик', u'Телефон: %s \nНазвание продукта: %s' %(phone, product.name), u"jcdeesign@gmail.com", [u"mozger@ukr.net", u"sanjok744@gmail.com"])
    # msg.send()

    return HttpResponse('ok')


@never_cache
def noclick(request):
    phone = str(request.POST['phone'])
    email = str(request.POST['email'])
    name = str(request.POST['name'])
    product_id = int(request.POST['product_id'])

    product = get_object_or_404(Product, id=product_id)

    quikorder = NoOrder(product=product, phone=phone, pub_date=datetime.datetime.now(), email=email, name=name, producttext=product.name)
    quikorder.save()

    # msg = EmailMessage('Покупка в 1 клик', u'Телефон: %s \nНазвание продукта: %s' %(phone, product.name), u"jcdeesign@gmail.com", [u"mozger@ukr.net", u"sanjok744@gmail.com"])
    # msg.send()

    return HttpResponse('ok')


@never_cache
def clear_cache(request):
    # assert False, 1
    products = Product.objects.all()
    for product in products:
        product.colors = None
        product.save()
    return HttpResponse('ok')


@never_cache
def get_cities(request):
    from grab import Grab
    import json
    g = Grab()
    g.setup(post='{"apiKey": "5cc30191313ca719c44feaba950d9165","modelName": "Address","calledMethod": "getCities","methodProperties": {}}')
    g.go('https://api.novaposhta.ua/v2.0/json/')
    items = []
    # assert False, g.go('https://api.novaposhta.ua/v2.0/json/').body
    for item in json.loads(g.response.body)['data']:
        one = {'name': item['DescriptionRu'], 'value': item['Ref']}
        items.append(one)


    data = json.dumps(items)

    return HttpResponse(data, content_type="application/json")

@never_cache
def get_warehouses(request):
    from grab import Grab
    import json
    g = Grab()

    city = request.POST.get('city','06f87968-4079-11de-b509-001d92f78698')
    g.setup(post='{"modelName": "Address","calledMethod": "getWarehouses","methodProperties": { "CityRef": "' + city + '"},"apiKey": "5cc30191313ca719c44feaba950d9165"}')
    g.go('https://api.novaposhta.ua/v2.0/json/')
    items = []

    # assert False, g.response.body


    for item in json.loads(g.response.body)['data']:
        one = {'name': item['DescriptionRu'], 'value': item['Number']}
        items.append(one)


    data = json.dumps(items)

    return HttpResponse(data, content_type="application/json")

@never_cache
def dublies(request):
    products = Product.objects.all()
    colors = ColorProduct.objects.all()

    pdublies = []

    for product in products:
        # items = []
        pitems = []
        citems = []

        colproduct = Product.objects.filter(idname = product.idname).count()
        colcolor = ColorProduct.objects.filter(idname = product.idname).count()
        allcol = colproduct + colcolor
        if allcol > 1:
            dubproducts = Product.objects.filter(idname = product.idname)
            dubcolors = ColorProduct.objects.filter(idname = product.idname)

            pdublies.append({
                'item': product.name,
                'dubproducts': dubproducts,
                'dubcolors' : dubcolors,
            })

            # for oneitem in dubcolors:
    assert False, pdublies

@never_cache
def get_category_filters(request):
    if request.user.is_authenticated() and request.user.is_admin:
        id = request.POST.get('id', 0)
        item = get_object_or_404(Category, pk=id)
        data = json.dumps({
            'filters':item.get_filters_json,
            'brands' :item.get_brands_json,
            })

        return HttpResponse(data, content_type="application/json")
    else:
        redirect('/')


@never_cache
def allcomplects(request):
    if request.user.is_authenticated() and request.user.is_admin:
        return render(request, 'allcomplects.html', {})
    else:
        redirect('/')



@never_cache
def allactions(request):
    if request.user.is_authenticated() and request.user.is_admin:
        return render(request, 'allactions.html', {})
    else:
        redirect('/')

@never_cache
def getcatcomplect(request):
    if request.user.is_authenticated() and request.user.is_admin:
        id = request.POST.get('id', 0)
        item = get_object_or_404(Category, pk=id)
        data = json.dumps({
            'items' : item.get_colors_json,
            'brands' : item.get_brands_json,
            'complects': item.get_complects_json,
            })

        return HttpResponse(data, content_type="application/json")
    else:
        redirect('/')

@never_cache
def getcattree(request):
    if request.user.is_authenticated() and request.user.is_admin:

        from django.db.models import Q
        import operator
        def get_queryset_descendants(nodes, include_self=False):
           if not nodes:
               return Category.tree.none()
           filters = []
           for n in nodes:
               lft, rght = n.lft, n.rght
               if include_self:
                   lft -= 1
                   rght += 1
               filters.append(Q(tree_id=n.tree_id, lft__gt=lft, rght__lt=rght))
           q = reduce(operator.or_, filters)
           return Category.objects.filter(q)

        items = Category.objects.filter(level=0, published=True).order_by("-ordering")

        items = get_queryset_descendants(items, True)

        results = []

        for item in items:
            if item.level == 0:
                name = item.name

            if item.level == 1:
                name = "--" + item.name

            if item.level == 2:
                name = "----" + item.name

            if item.level == 3:
                name = "------" + item.name

            if item.level == 4:
                name = "--------" + item.name

            results.append({'name': name, 'value': item.id})

        data = json.dumps(results)

        return HttpResponse(data, content_type="application/json")

    else:
        redirect('/')

def createcomplect(request):
    if request.user.is_authenticated() and request.user.is_admin:
        maincat = request.POST.get('maincat')
        cat = request.POST.get('categories')
        brand = request.POST.get('brand', 0)
        percent = int(request.POST.get('percent'))

        mainitemsactive = []
        itemsactive = []

        mainitems = ColorProduct.objects.filter(product__category_id = int(maincat))
        items = ColorProduct.objects.filter(product__category_id = int(cat))

        for one in mainitems:
            if request.POST.get("item_" + str(one.id)):
                mainitemsactive.append(one)

        for one in items:
            if request.POST.get("item_" + str(one.id)):
                itemsactive.append(one)

        # assert False,

        for main in mainitemsactive:
            for one in itemsactive:
                if not Complect.objects.filter(name = main.productname + ' ' + one.productname):
                    comp = Complect(name = main.productname + ' ' + one.productname)
                    comp.save()
                    oneitem = ComplectItem(product=main, complect=comp, order=1)
                    oneitem.save()

                    oneitem = ComplectItem(product=one, complect=comp, order=2, percent=percent)
                    oneitem.save()

        return HttpResponse('ok')
    else:
        return redirect('/')
        # assert False, itemsactive
        # pass


def deletecomplect(request):
    if request.user.is_authenticated() and request.user.is_admin:
        id = int(request.POST.get('id', 0))
        if id:
            complect = Complect.objects.filter(id=id)
            if complect:
                complect.delete()

        return HttpResponse('ok')
    else:
        return redirect('/')


def ugcsv(request):
    items = Uproduct.objects.all()

    return render(request, 'shop/ugcsv.html', {
        'items':items,
    })



@never_cache
def getdocument(request):
    if request.user.is_authenticated() and request.user.is_admin:
        items = Category.objects.filter(level = 0, published=True)
        return render(request, 'shop/document.html', {'items': items})
    else:
        raise Http404


@never_cache
def real_time_price(request, id):
    price = ColorProduct.objects.get(id=int(id)).price
    items = { 
            "items": [{
                "price": str(price),
            }]
        }
    return HttpResponse(json.dumps(items), content_type="application/json")
