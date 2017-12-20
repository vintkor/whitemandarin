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
from .models import *
from shop.models import *
# import json
import json
import datetime
import base64
import random
from django.contrib.auth import authenticate, login
import csv
import StringIO
from django.utils.encoding import smart_unicode

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
def scan_it(request):
    if request.user.is_admin:

        id = int(request.POST.get('id',0))

        category = Category.objects.filter(pk=id)

        if category:

            cat = category.get()

            items = len(ColorProduct.objects.filter(product__category=cat))
            scan = ScanHotline(category=cat, items=items)
            scan.save()

        # envpath = "/var/www/env/20k/bin/python"
        # managepath = "/var/www/20k_new/www/cms/manage.py"
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
            items = OneHotline.objects.filter(scan=scan)

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
                    'href': item.product.href,
                    'hrefok': item.product.hrefok,
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

            ids.append(item.id)

            href = request.POST.get("href_" + str(item.id), '')
            hrefok = request.POST.get("hrefok_" + str(item.id), 0)

            if href:
                item.href = href
                item.hrefok = hrefok
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


    # pass
