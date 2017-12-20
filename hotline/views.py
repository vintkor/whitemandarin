# -*- coding: utf-8 -*-
# from django.db import models
import subprocess
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
from django.utils import timezone
from .models import *
from shop.models import *
from pymongo import MongoClient
# import json
import json
import datetime
import base64
import random
from django.contrib.auth import authenticate, login
import csv
import StringIO
from django.utils.encoding import smart_unicode
from grab import Grab

# import unicodecsv
# from easy_thumbnails.files import get_thumbnailer

@never_cache
def lastscan(request):
    if request.user.is_admin:

        last = ScanHotline.objects.all().order_by('-pub_date')[:1].get()

        # assert False, last.pub_date

        items = OneHotline.objects.filter(scan=last)

        # assert False, last


        # from django.core import mail

        # emails = (('Hey Man', "I'm The Dude! So that's what you call me.", "ageyevaelena@gmail.com", ["mozger@ukr.net"]),
        #  ('Dammit Walter', "Let's go bowlin'.", 'ageyevaelena@gmail.com', ["mozger@ukr.net"]),)
        # results = mail.send_mass_mail(emails)

        # assert False, results




        return render(request, 'hotline/lastscan.html', {'items': items})


@never_cache
def lastscan_remote(request):
    if request.user.is_admin:
        strongs = Concurent.objects.filter(strong=True)
        result = []
        if strongs:
            for strong in strongs:
                result.append(str(strong.itemid))
            # assert False,result
            result = ','.join(result)
        else:
            result = 0

        # items = OneHotline.objects.filter(scan=last)
        return render(request, 'hotline/lastscan_remote.html', {'strongs': result})


@never_cache
def scan_it(request):
    if request.user.is_admin:

        id = int(request.POST.get('id',0))

        category = Category.objects.filter(pk=id)

        if category:

            cat = category.get()

            items = len(ColorProduct.objects.filter(product__category=cat))
            scan = ScanHotline(category=cat, items=items)
            scan.save()

        # envpath = "/var/www/env/20K/bin/python"
        # managepath = "/var/www/20K_new/www/cms/manage.py"
        # comandname = "scanhotline"
        # path = envpath + ' ' + managepath + ' ' + comandname + ' ' + str(request.POST.get('id', 0))
        # # assert False, path
        # # print subprocess.call(path, shell=True)
        # import os
        # os.seteuid(0)
        # os.system(path)
        return HttpResponse('ok')

@never_cache
def get_category_data(request):
    if request.user.is_admin:

        category_id = int(request.POST.get('id', 0))
        category = Category.objects.filter(pk=category_id).get()
        scans = ScanHotline.objects.filter(category_id=category_id).order_by('pub_date')
        results = {'scans': [], 'items': [], 'name': category.name,}

        for scan in scans:
            results['scans'].append({
                'id': scan.id,
                'date': str(scan.pub_date),
                })
                          # <td>{{ item.product.name }}</td>
                          # <td>{{ item.min }}</td>
                          # <td>{{ item.max }}</td>
                          # <td>{{ item.position }}</td>
                          # <td>{{ item.total }}</td>
                          # <td>{{ item.product.price }}</td>
                          # <td><input type="text" name="product_{{ item.product.id }}" value="{{ item.product.price}}"></td>
                          # <td><input type="text" name="href_{{ item.product.id }}" value="{{ item.product.href }}"></td>
                          # <td><input type="checkbox" name="hrefok_{{ item.product.id }}" value="1"></td>
        # assert False, scan.id
        if scans:
            items = OneHotline.objects.filter(scan=scan).order_by('-product__marga')

            # assert False, len(items)

            for item in items:

                oneposition = {
                    'checkid': item.id,
                    'product_id': item.product.id,
                    'product_name': item.product.productname,
                    'min': item.min,
                    'max': item.max,
                    'total': item.total,
                    'price': str(item.product.price),
                    'price_in': str(item.product.price_in),
                    'price_rrc': str(item.product.price_rrc),
                    'price_rrc_ok': item.product.price_rrc_ok,
                    'href': item.product.href,
                    'hrefok': item.product.hrefok,
                    'marga': item.product.marga,
                    'position': item.position,
                    'concurents': '',
                }

                if item.concurents:
                    oneposition['concurents'] = json.loads(item.concurents)

                results['items'].append(oneposition)

            results['data'] = str(scan.pub_date.strftime("%d.%m.%y ") + str(int(scan.pub_date.strftime("%H")) + 3) + ':' + scan.pub_date.strftime("%M"))

        # assert False, results
            results['firms'] = list(scan.getallfirms())
        data = json.dumps(results)


        return HttpResponse(data, content_type="application/json")


@never_cache
def get_category_data_remote(request):
    if request.user.is_admin:

        category_id = int(request.POST.get('id', 0))
        category = Category.objects.filter(pk=category_id).get()
        results = {'items': [], 'name': category.name, }
        firms = []
        firmsresult = {}

        items = ColorProduct.objects.filter(product__category=category, price__gt=0)
        i = 0

        for item in items:
            # assert False, item.lastscan
            i += 1
            oneposition = {
                'checkid': i,
                'product_id': item.id,
                'product_name': item.productname,
                'price': str(item.price),
                'price_in': str(item.price_in),
                'price_rrc': str(item.price_rrc),
                'price_rrc_ok': item.price_rrc_ok,
                'href': item.href,
                'hrefok': item.hrefok,
                'marga': str(item.marga),
                # 'position': item.position,
                'concurents': [],
                'date': str(item.lastscan_date)
            }
            if item.lastscan:
                oneposition['concurents'] = json.loads(item.lastscan)

            results['items'].append(oneposition)

            for concurent in item.concurents.all():
                if concurent not in firms:
                    firms.append(concurent)

        for firm in firms:
            firmsresult[firm.itemid] = firm.name

        results['date'] = str(category.lastscan_date.strftime("%d.%m.%Y ")) + str(int(category.lastscan_date.strftime("%H")) + 3) + str(category.lastscan_date.strftime(":%M:%S"))
        results['name'] = category.name
        results['id'] = category.id
        results['firms'] = firmsresult
        data = json.dumps(results)

        return HttpResponse(data, content_type="application/json")



@never_cache
def get_category(request):
    if request.user.is_admin:

        id = request.GET.get('id', 0)
        try:
            id = int(id)
            data = {'parent_id': id}
        except:
            data = {'level': 0}
            # id = False
        items = Category.objects.filter(**data)
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
def savecat(request, id):
    if request.user.is_admin:
        category = Category.objects.filter(pk=int(id))
        ids = []
        items = ColorProduct.objects.filter(price__gt=0, product__category=category)

        # assert False, items

        for item in items:

            # ids.append(item.id)

            href = request.POST.get("href_" + str(item.id), '')
            hrefok = request.POST.get("hrefok_" + str(item.id), 0)
            try:
                price = int(request.POST.get("product_" + str(item.id), 0).split('.')[0])
            except:
                price = 0
            # assert False, price

            if href:
                item.href = href
                item.hrefok = hrefok
                item.price = price

                if item.main:
                    item.product.price = price
                    item.product.save()
                item.save()

        # assert False, ids

        return HttpResponse('ok')


@never_cache
def get_not_active(request, id):

    items = ColorProduct.objects.filter(Q(product__published=False) | Q(price=0), product__category_id=id)
    results = []
    for item in items:
        results.append(item.productname.strip())
    # assert False, items

    data = json.dumps(results)

    return HttpResponse(data, content_type="application/json")

@never_cache
def getprice(request):
    pass


@never_cache
def get_status(request):

    return HttpResponse('ok')
    active = ScanHotline.objects.filter(started=True, finished=False)
    queried = ScanHotline.objects.filter(started=False, finished=False)

    results = {
        'activecat':  False,
        'items' : False,
        'nowitems': False,
        'queried' : False,
        }

    if active:
        results['activecat'] = active[0].category.name,
        results['items'] = active[0].items,
        results['nowitems'] = active[0].nowitems,

    if queried:
        results['queried'] = []
        for one in queried:
            results['queried'].append(one.category.name)
    data = json.dumps(results)

    return HttpResponse(data, content_type="application/json")


@never_cache
def scan_it_remote(request):
    if request.user.is_admin:
        siteremote = "http://hotline.gowius.com/addtask/"
        site = '20k.com.ua'

        id = int(request.POST.get('id',0))

        category = Category.objects.filter(pk=id)

        if category:

            cat = category.get()

            items = ColorProduct.objects.filter(product__category=cat)
            result = []
            # scan = ScanHotline(category=cat, items=items)
            # scan.save()
            for item in items:
                if item.href and item.price > 0 and item.hrefok:
                    result.append({'id': item.id, 'url': item.href})

            g = Grab()
            g.setup(post={'url': site, 'items': json.dumps(result)})
            g.go(siteremote)

    return HttpResponse('ok')


@never_cache
def set_remote_data(request):
    result = request.POST.get('result','')
    # assert False, result
    if result:
        result = json.loads(result)
        for firm in result['firms']:
            if not Concurent.objects.filter(itemid=firm['firm_id']):
                Concurent(itemid=firm['firm_id'], name=firm['name']).save()
            # assert False, firm
        for item in result['items']:

            firms_ids = []
            if 'prices' in item:
                for f in item['prices']:
                    firms_ids.append(f['firm_id'])

            firms = Concurent.objects.filter(itemid__in=firms_ids)

            colors = ColorProduct.objects.filter(href=item['url'])
            for color in colors:
                # assert False, item['prices']
                if "prices" in item:
                    color.lastscan = json.dumps(item['prices'])
                color.lastscan_date = timezone.now()
                color.concurents.clear()
                color.concurents = firms
                color.save()

                lastcolor = color

        category = lastcolor.product.category

        category.lastscan_date = datetime.datetime.now()
        category.save()



    return HttpResponse('ok')



@never_cache
def showstatus(request):
    g = Grab()
    g.setup(post = {"name": "20k.com.ua"})
    g.go("http://hotline.gowius.com/showstatus/")
    return HttpResponse(g.response.body)


@never_cache
def showproduct(request):
    client = MongoClient()
    url = request.POST.get('url', '')
    filters = []
    if url:
        product = client.hotline.hotproduct.find_one({'url': url})
        category = client.hotline.hotcategory.find_one({'_id': product['category']})

        for f in product['filters']:
            # assert False, f
            filter = client.hotline.hotfiltersitems.find_one({'hid': f})
            filter['mainfilter'] = client.hotline.hotfilters.find_one({'_id': filter['filter']})

            filters.append(filter)


            # assert False, filter
    return render(request, 'hotline/showproduct.html', {'product': product, 'category': category, 'filters': filters})


@never_cache
def recat(request):
    items = Category.objects.filter(hotlineurl__isnull=False)
    return render(request, 'hotline/recat.html', {'items': items})
