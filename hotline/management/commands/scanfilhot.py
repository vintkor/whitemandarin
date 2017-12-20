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

        cat_id = category.find_one({'url': url})['_id']

        mainfilters = list(filterdb.find({'category': ObjectId(cat_id)}))

        for mainfilter in mainfilters:

            onefilters = filteritemdb.find({'filter': ObjectId(mainfilter['_id']), 'finished': False})

            for onef in onefilters:
                finished = True

                self.stdout.write(onef['href'] + ": " + str(onef['hid']))

                goog = Grab(log_file='/tmp/log.html')
                goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
                goog.go("http://hotline.ua" + onef['href'])

                itemscount = float(goog.doc.pyquery('h2.selected-filtrs.grey-6')[0].text.split(' ')[1].strip())
                pages = int(math.ceil(itemscount/24))

                self.stdout.write('Url: ' + onef['href'] + ', Pages:' + str(pages))

                productlinks = goog.doc.pyquery('.cell.gd b.m_r-10 > a.g_statistic')
                if goog.doc.pyquery('.g-recaptcha').eq(0):
                    finished = False
                    # print('captcha error')
                    # # proxy.active=False
                    # # proxy.save()
                    # send_mail(pg.config['proxy'], body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
                    # return

                for productlink in productlinks:
                    producturl = productlink.attrib['href']
                    self.stdout.write(producturl)

                    item = product.find_one({'url': producturl})
                    if not 'filters' in item:
                        item['filters'] = []
                    item['filters'].append(onef['hid'])

                    product.update({'url': producturl}, item)

                for i in range(1, pages):
                    goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
                    goog.go("http://hotline.ua" + onef['href'] + '?p=' + str(i))

                    self.stdout.write("http://hotline.ua" + onef['href'] + '?p=' + str(i))

                    # itemscount = float(goog.doc.pyquery('h2.selected-filtrs.grey-6')[0].text.split(' ')[1].strip())
                    # pages = int(math.ceil(itemscount/24))
                    productlinks = goog.doc.pyquery('.cell.gd b.m_r-10 > a.g_statistic')

                    if goog.doc.pyquery('.g-recaptcha').eq(0):
                        finished = False

                    for productlink in productlinks:
                        producturl = productlink.attrib['href']
                        self.stdout.write(producturl)

                        item = product.find_one({'url': producturl})
                        if not 'filters' in item:
                            item['filters'] = []

                        if not onef['hid'] in item['filters']:
                            item['filters'].append(onef['hid'])

                        product.update({'url': producturl}, item)

                if onef['finished'] != finished:
                    onef['finished'] = finished
                    product.update({'href': onef['href']}, onef)
                    # productitem = get_hotline_data('http://hotline.ua' + producturl, False, False)
                    # productitem['category'] = ObjectId(cat_id)
                    # product.insert_one(productitem)
                    # assert False, productitem
                    # product.update({'url': producturl}, productitem, {'upsert': False})


                # assert False, itemscount
        # pquery = pq(goog.response.body)

        # categoryname = pquery('h1.title-24.p_b-10')[0].text

        # cat_id = category.insert_one({
        #     'name': categoryname,
        #     'count': itemscount,
        #     'pages': pages,
        #     'url': url}).inserted_id

        # # assert False, itemscount


        # names = pquery('#filters > .cell.f-title')

        # f = open(PROJECT_PATH + '/../4.txt', 'w+')

        # f.write(goog.response.body)

        # # assert False, len(names)
        # i=0
        # for name in names:
        #     # fitems = names[i]
        #     fitemstr = pquery('#filters > .cell.full-list').eq(i)

        #     # assert False, fitemstr


        #     if name.text:
        #         nametext = name.text.strip()
        #         if not nametext in itemsname:

        #             fi = {'name': nametext, 'category': ObjectId(cat_id)}
        #             fi['items'] = []

        #             for fitem in pq(fitemstr)('.f-item > a'):
        #                 fitext = fitem.text.strip()
        #                 href = fitem.attrib['href']
        #                 fid = int(href.split('/')[3])

        #                 filteriteminserted = filteritemdb.insert_one({'name': fitext, 'href': href, 'hid': fid, '_id':
        #                     ObjectId() }).inserted_id
        #                 fi['items'].append(filteritemdb.find_one({'_id': filteriteminserted}))

        #             filterinserted = filterdb.insert_one(fi)

        #             itemsname.append(fi)
        #         import codecs
        #         with codecs.open(PROJECT_PATH + '/../5.txt', "w", encoding="utf-8") as f:
        #             f.write(unicode(fitemstr))

        #     i+=1
        # # for item in itemsname:

        # for i in range(1, pages+1):
        #     self.stdout.write('Page now: ' + str(i))

        #     goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
        #     goog.go("http://hotline.ua" + url + "?p=" + str(i))


        #     # self.stdout.write(str(i))



        # # # assert False, itemsname
        # #     i+=1
        # # # f = open(, 'w+')

        # # # f.write(goog.response.body)
