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
        propertydb = db.hotproperty
        settingdb = db.hotsettings

        if settingdb.find_one({'name': 'status'}):
            settingdb.update({'name': "status"}, {"value": "started", "name": "status"})
        else:
            settingdb.insert_one({"value": "started", "name": "status"})

        product.remove({"name": ""})

        # assert False, args[0]
        url = args[0]
        if len(args) > 1:
            direction = args[1]
        else:
            direction = 0
        msg = ""
        error = ""

        itemsname = []
        itemsvalues = []



        # goog = Grab(log_file='/tmp/log.html')
        # goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
        goog = scanhot("http://hotline.ua" + url)

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

            # if direction:
            index = i - int(direction)

            if index >= 0:


                fitemstr = pquery('#filters > .cell.full-list').eq(index)

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

        # return

        for i in range(0, pages):
            self.stdout.write('Page now: ' + str(i))

            settingdb.update({'name': "status"}, {"value": "Category: " + categoryname + ". Scanning product page:" + str(i) + " From:" + str(pages), "name": "status"})


            pageurl = "http://hotline.ua" + url + "?p=" + str(i)

            # goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
            goog = scanhot(pageurl)



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

        # second action

        cat_id = category.find_one({'url': url})['_id']

        mainfilters = list(filterdb.find({'category': ObjectId(cat_id)}))

        for mainfilter in mainfilters:

            onefilters = list(filteritemdb.find({'filter': ObjectId(mainfilter['_id']), 'finished': False}))

            for onef in onefilters:
                finished = True

                self.stdout.write(onef['href'] + ": " + str(onef['hid']))

                # goog = Grab(log_file='/tmp/log.html')
                # goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
                # goog.go("http://hotline.ua" + onef['href'])

                goog = scanhot("http://hotline.ua" + onef['href'])

                try:
                    itemscount = float(goog.doc.pyquery('h2.selected-filtrs.grey-6')[0].text.split(' ')[1].strip())
                    pages = int(math.ceil(itemscount/24))
                except Exception, e:
                    pages = 1
                    # raise e

                self.stdout.write('Url: ' + onef['href'] + ', Pages:' + str(pages))

                productlinks = goog.doc.pyquery('.cell.gd b.m_r-10 > a.g_statistic')
                # if goog.doc.pyquery('.g-recaptcha').eq(0):
                #     finished = False
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

                    settingdb.update({'name': "status"}, {"value": "Category: " + categoryname + ". Scanning filter " + mainfilter['name'] + ":" + onef['name'] + " page:" + str(i) + " from:" + str(pages), "name": "status"})

                    # goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
                    # goog.go("http://hotline.ua" + onef['href'] + '?p=' + str(i))

                    # self.stdout.write("http://hotline.ua" + onef['href'] + '?p=' + str(i))
                    goog = scanhot("http://hotline.ua" + onef['href'] + '?p=' + str(i))
                    # itemscount = float(goog.doc.pyquery('h2.selected-filtrs.grey-6')[0].text.split(' ')[1].strip())
                    # pages = int(math.ceil(itemscount/24))
                    productlinks = goog.doc.pyquery('.cell.gd b.m_r-10 > a.g_statistic')

                    if goog.doc.pyquery('.g-recaptcha').eq(0):
                        finished = False

                    for productlink in productlinks:
                        producturl = productlink.attrib['href']
                        self.stdout.write(producturl)

                        item = product.find_one({'url': producturl})
                        if item:
                            if not 'filters' in item:
                                item['filters'] = []

                            if not onef['hid'] in item['filters']:
                                item['filters'].append(onef['hid'])

                            product.update({'url': producturl}, item)
                        else:
                            error += "Not Found: " + producturl + ", " + onef['href'] + "\n"
                if onef['finished'] != finished:
                    onef['finished'] = finished
                    product.update({'href': onef['href']}, onef)

        # import codecs
        # with codecs.open(PROJECT_PATH + '/../error.txt', "w", encoding="utf-8") as f:
        #     f.write(error)

# thid action

        cat_id = category.find_one({'url': url})['_id']

        products = list(product.find({'category': ObjectId(cat_id)}))

        for oneproduct in products:
            self.stdout.write(oneproduct['url'])
            for prop in oneproduct['properties']:
                propname = prop['name']
                # self.stdout.write(propname)
                if not propertydb.find_one({'name': propname, 'category': ObjectId(cat_id)}):
                    propertydb.insert_one({'name': propname, 'category': ObjectId(cat_id)})

        for one in products:
            for prop in one['properties']:
                if prop['name'] == u"Производитель":
                    self.stdout.write(prop['prop'])
                    one['brand'] = prop['prop']
                    product.update({'url': one['url']}, one)
