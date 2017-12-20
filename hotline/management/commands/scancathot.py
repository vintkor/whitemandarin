# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Poll
from grab import Grab
import re
import urllib
import datetime
import json
from shop.models import *
from hotline.models import *
# from .models import *
import time
import urllib
import random
from cms.settings import *
from hotline.utils import *
from pyquery import PyQuery as pq
import codecs
from cms.local_settings import PROJECT_PATH
from django.db.models import Q
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient()
db = client.hotline
from hotline.utils import *
import math




class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        filterdb = db.hotfilters
        filteritemdb = db.hotfiltersitems
        category = db.hotcategory
        product = db.hotproduct

        url = "/mobile/umnye-chasy-smartwatch/"
        msg = ""

        itemsname = []
        itemsvalues = []

        goog = Grab(log_file='/tmp/log.html')
        goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
        goog.go("http://hotline.ua" + url)

        pquery = pq(goog.response.body)

        categoryname = pquery('h1.title-24.p_b-10')[0].text
        itemscount = float(pquery('h2.selected-filtrs.grey-6')[0].text.split(':')[1].strip())
        pages = int(math.ceil(itemscount/24))

        catdata = category.find_one({'url': url})

        if catdata:
            cat_id = catdata['_id']
            msg += u"Category used: " + categoryname + u" .Used proxy: " + goog.config['proxy'] + '\n'

        else:
            cat_id = category.insert_one({
                'name': categoryname,
                'count': itemscount,
                'pages': pages,
                'url': url}).inserted_id
            msg += u"Category created: " + categoryname + u" .Used proxy: " + goog.config['proxy'] + '\n'

        # assert False, itemscount


        names = pquery('#filters > .cell.f-title')

        i=0
        for name in names:
            fitemstr = pquery('#filters > .cell.full-list').eq(i)

            if name.text:
                nametext = name.text.strip()
                if not nametext in itemsname:
                    filteritem = filterdb.find_one({'name': nametext, 'category': ObjectId(cat_id)})
                    if filteritem:
                        filterinserted_id = filteritem['_id']
                        msg += u"Filter used: " + nametext + " .Used proxy: " + goog.config['proxy'] + '\n'

                    else:
                        fi = {'name': nametext, 'category': ObjectId(cat_id)}
                        msg += u"Filter created: " + nametext + " .Used proxy: " + goog.config['proxy'] + '\n'
                        filterinserted_id = filterdb.insert_one(fi).inserted_id

                    for fitem in pq(fitemstr)('.f-item > a'):
                        fitext = fitem.text.strip()
                        href = fitem.attrib['href']
                        fid = int(href.split('/')[3])
                        filteritem = filteritemdb.find_one({'href': href})
                        if not filteritem:
                            filteriteminserted = filteritemdb.insert_one({'name': fitext, 'href': href, 'hid': fid, 'filter': ObjectId(filterinserted_id), 'finished': False})
            i+=1


        for i in range(0, pages):
            self.stdout.write('Page now: ' + str(i))

            goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
            goog.go("http://hotline.ua" + url + "?p=" + str(i))

            productlinks = pquery(goog.response.body)('.cell.gd b.m_r-10 > a.g_statistic')

            for productlink in productlinks:
                producturl = productlink.attrib['href']
                tempproduct = product.find_one({'url': producturl})
                if tempproduct:
                    msg += u"Product used: " + tempproduct['name'] + " .Used proxy: " + goog.config['proxy'] + '\n'
                else:

                    self.stdout.write(producturl)
                    productitem = get_hotline_data('http://hotline.ua' + producturl, False, False)
                    msg += u"Product created: " + productitem['name'] + " .Used proxy: " + goog.config['proxy'] + '\n'
                    productitem['category'] = ObjectId(cat_id)
                    product.insert_one(productitem)

        self.stdout.write(msg)
        send_mail('Scan category:' + url, msg, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
