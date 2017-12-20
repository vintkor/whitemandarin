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
from django.views.decorators.cache import never_cache
from .models import *
import json
import datetime
import base64
import random
import dropbox
from django.contrib.auth import authenticate, login
import csv
import StringIO
from django.utils.encoding import smart_unicode
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
# import unicodecsv
# from easy_thumbnails.files import get_thumbnailer
import xlrd
import urllib
from django.db.models import Q
import operator
# import cms.settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import requests
client = MongoClient()
db = client.hotline
from django.shortcuts import render
from shop.models import *



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



# Create your views here.
@never_cache
def allfiltershotline(request):
    hotitems = db.hotcategory.find().sort([('name', 1)])
    items = Category.objects.filter(level=0, published=True).order_by("-ordering")
    items = get_queryset_descendants(items, True)

    return render(request, 'shop/allfiltershotline.html', {
        "items": items,
        'hotitems': hotitems})





@user_passes_test(lambda u: u.is_admin)
@never_cache
def get_filters_properties(request, id):

    category = Category.objects.get(pk=id)

    result = json.dumps({
        'filters': category.get_all_filters,
        'properties': category.get_all_properties,
        'hotlineurl': category.hotlineurl,
        })

    return HttpResponse(result, content_type="application/json")


@user_passes_test(lambda u: u.is_admin)
@never_cache
def deletepropertiesfilters(request):
    data = json.loads(request.body)
    # assert False, data
    category = Category.objects.get(pk=data['id'])
    for f in category.filters.all():
        if unicode(f.id) in data['filters'] and data['filters'][unicode(f.id)]:
            category.filters.remove(f)

    for p in category.properties.all():
        if unicode(p.id) in data['properties'] and data['properties'][unicode(p.id)]:
            category.properties.remove(p)

    category.save()
    # assert False, category.get_all_filters

    result = json.dumps({
        'filters': category.get_all_filters,
        'properties': category.get_all_properties,
        })

    return HttpResponse(result, content_type="application/json")



@user_passes_test(lambda u: u.is_admin)
@never_cache
def copypropertiesfilters(request):

    # filterdb = db.hotfilters
    # filteritemdb = db.hotfiltersitems
    # category = db.hotcategory
    # product = db.hotproduct
    # propertydb = db.hotproperty
    data = json.loads(request.body)
    # assert False, data
    category = Category.objects.get(pk=data['cid'])

    hotcat = db.hotcategory.find_one({'_id': ObjectId(data['hid'])})

    category.hotlineurl = hotcat['url']
    category.save()
    # get all hotfilters
    # create filter in the site
    # get subfilters
    # create subfilters in the site
    # add filter to the category
    i = 1
    for f in db.hotfilters.find({'category': ObjectId(data['hid'])}):
        # assert False, data['hotfilters'][str÷(f['_id'])]
        if data['hotfilters'][str(f['_id'])]:
            if not category.filters.all().filter(name=f['name']):

                i2 = 1
                newf = Filter(name=f['name'], ordering=i, requery=True)
                newf.save()
                i += 1
                for fi in db.hotfiltersitems.find({'filter': ObjectId(f['_id'])}):
                    FilterSelect(filter=newf, value=fi['name'], ordering=i2).save()
                    i2 += 1
                category.filters.add(newf)
    i = 1
    for p in db.hotproperty.find({'category': ObjectId(data['hid'])}):
        if data['hotproperties'][str(p['_id'])]:
            if not category.properties.all().filter(name=p['name']):
                newp = Property(name=p['name'], ordering=i)
                newp.save()
                i += 1
                category.properties.add(newp)
    # for p in category.properties.all():
    #     if data['properties'][unicode(p.id)]:
    #         category.properties.remove(p)

    category.save()
    # assert False, category.get_all_filters

    result = json.dumps({
        'filters': category.get_all_filters,
        'properties': category.get_all_properties,
        })

    return HttpResponse(result, content_type="application/json")


@user_passes_test(lambda u: u.is_admin)
@never_cache
def get_hotline_filters_properties(request, id):
    hotfilters = list(db.hotfilters.find({'category': ObjectId(id)}))
    hotproperties = list(db.hotproperty.find({'category': ObjectId(id)}))

    result = json_util.dumps({
        'hotfilters': hotfilters,
        'hotproperties': hotproperties,
        })

    return HttpResponse(result, content_type="application/json")


@user_passes_test(lambda u: u.is_admin)
@never_cache
def price(request):

    settings = {}
    provider = int(request.GET.get('provider', 0))
    type = int(request.GET.get('type', 2))
    name = request.GET.get('name', '')

    types = [
        {'name': u'Несоеденное', 'id': 0},
        {'name': u'Соеденное', 'id': 1},
        {'name': u'Все', 'id': 2}
    ]

    providers = Provider.objects.all()


    if provider:
        settings['provider_id'] = provider

    if type != 2:
        settings['linked'] = type

    if name:
        settings['searchindex__search'] = name

    if settings:
        items = PriceString.objects.filter(**settings).order_by('linked')
    else:
        items = []


    per_page = 200
    page = request.GET.get('page', 0)

    # assert False, results_items

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


    newpath = "/price/?provider=" + str(provider) + "&type=" + str(type)

    return render(request, 'price/price.html', {'items': items, 'providers':providers, 'provider': provider, 'type': type, 'types':types, 'name': name, 'newpath': newpath})


@user_passes_test(lambda u: u.is_admin)
@never_cache
def createconnection(request):
    c_id = int(request.POST.get('c_id', 0))
    s_id = int(request.POST.get('s_id', 0))

    ps = PriceString.objects.get(pk=s_id)
    cp = ColorProduct.objects.get(pk=c_id)
    if ps and cp:

        # temp = ColorPrice.objects.filter(pricestring=ps, colorproduct=cp)

        if cp.price_connected and s_id in cp.price_connected:
            # temp[0].delete()
            ps.linked = False
            cp.price_connected.remove(s_id)
            # cp.price_in = 0
            # cp.save()

        else:
            # ColorPrice(pricestring=ps, colorproduct=cp, user_id=request.user.id).save()
            ps.linked = True
            if cp.price_connected:
                cp.price_connected.append(s_id)
            else:
                cp.price_connected = [s_id]

            if not cp.product.articul:
                cp.product.articul = ps.articul
                cp.product.save()
            # cp.price_in = ps.last_price_grn
            # cp.save()

            # ps.update_price()

        ps.save()
        cp.save()


        # assert False, ps.linked

    return HttpResponse(json.dumps(cp.price_connected), content_type="application/json")


@never_cache
def simplesearch(request):
    q = request.POST.get('q', '')
    s_id = int(request.POST.get('s_id', 0))
    connected_ids = []
    products = []
    active_price = []

    connected = ColorProduct.objects.filter(price_connected__contains=s_id)

    for c in connected:
        products.append({'id': c.id, 'name': c.product.name })
        connected_ids.append(c.id)
        if c.price_connected:
            for oneprice in c.price_connected:
                active_price.append(oneprice)

    items = ColorProduct.objects.filter(product__name__search=q).exclude(id__in=connected_ids)[:10]
    results = []
    for item in items:
        # for c in item.new_colors:
        results.append({'id': item.id, 'name': item.product.name})

    newitems = []
    # db.articles.find( { $text: { $search: "coffee" } } )

    hotitems = db.hotproduct.find({'$text': {'$search': q}}, { 'score': { '$meta': "textScore" } }).sort([('score', {'$meta': 'textScore'})]).limit(10)

    for item in hotitems:
        newitems.append({'name': item['name'], 'id': str(item['_id'])})

    fromprice = []


    pstring = get_object_or_404(PriceString, pk=s_id)
    if q != pstring.articul and pstring.articul:
        prices = PriceString.objects.filter(searchindex__icontains=pstring.articul).exclude(provider=pstring.provider)[:10]
    else:
        prices = PriceString.objects.filter(searchindex__icontains=q).exclude(provider=pstring.provider)[:10]
    # aprices = PriceString.objects.filter(pk__in=active_price).exclude()
    for p in prices:
        active = False
        if p.id in active_price:
            active = True

        fromprice.append({
            'id': p.pk,
            'active': active,
            'name': p.provider.name + ' ' + p.brand + ' ' + p.model + ' ' + p.articul,
        })

  # assert False, result
    data = json.dumps({'items': results, 'active': products, 'newitems': newitems, 'fromprice': fromprice})

    return HttpResponse(data, content_type="application/json")


@never_cache
def getdropname(request):
    dbx = dropbox.Dropbox('wrmOhbJl30AAAAAAAAAADEFQRtjDItHTdZMNb4xeJguVuINnPXWC3BjSG5n1Zw2T')
    path = '/price'
    directory = request.POST.get('directory', '')
    if directory:
        path += '/' + directory
    results = dbx.files_list_folder(path)

    items = []

    # assert False, results.entries[0]
    for r in results.entries:
        items.append(r.name)
        pass

    items.sort()

    data = json.dumps(items)
    return HttpResponse(data, content_type="application/json")


@never_cache
def getdropfile(request):

    directory = request.POST.get('directory', '')
    file = request.POST.get('file', '')

    fields = [
        'brand',
        'model',
        'model2',
        'model3',
        'articul',
        'description',
        'description2',
        'description3',
        'garantee',
        'price',
        'price_rrc',
        'availabilityrow', 
    ]

    items = []
    dbx = dropbox.Dropbox('wrmOhbJl30AAAAAAAAAADEFQRtjDItHTdZMNb4xeJguVuINnPXWC3BjSG5n1Zw2T')



    try:
        downloadresult = True
        md, res = dbx.files_download('/price/' + directory + '/' + file)
    except:
        downloadresult = False
        # raise e
    # print(f.path)
    # print md.content_hash
    # print len(res.content)

    if downloadresult:


        # if f.path.split('.')[-1] == "xls":

        xlsBook = xlrd.open_workbook(file_contents=res.content)
        # workbook = openpyxlWorkbook()

        for i in xrange(0, xlsBook.nsheets):
            item = {'name': 'Sheet ' + str(i), 'items': []}
            xlsSheet = xlsBook.sheet_by_index(i)
            # sheet = workbook.active if i == 0 else workbook.create_sheet()
            # sheet.title = xlsSheet.name

            for row in xrange(0, 20):
                rowitem = []
                for string in xrange(0, 34):
                    try:
                        rowitem.append(unicode(xlsSheet.cell_value(row, string)))
                    except:
                        pass
                item['items'].append(rowitem)

            items.append(item)

        data = json.dumps({'items': items, 'fields': fields})
        return HttpResponse(data, content_type="application/json") 

    return HttpResponse('Noresults', content_type="application/json")              