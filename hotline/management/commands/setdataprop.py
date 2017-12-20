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

import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import time
from lxml.etree import tostring


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)


class Command(BaseCommand):

    # def saveproduct

                    # self.stdout.write(producturl)
                    # productitem = get_hotline_data('http://hotline.ua' + producturl, False, False)
                    # msg += u"Product created: " + productitem['name'] + " .Used proxy: " + goog.config['proxy'] + '\n'
                    # productitem['category'] = ObjectId(cat_id)
                    # product.insert_one(productitem)



    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):



        def getproductsurl(pageurl):

            self.stdout.write("Get pages of product. Page: " + str(pageurls.index(pageurl)) + ', From:' + str(allpagesurls))

            allproductslinks = []
            goog = scanhot(pageurl)
            productlinks = pq(goog.response.body)('.cell.gd b.m_r-10 > a.g_statistic')
            for productlink in productlinks:
                producturl = productlink.attrib['href']
                tempproduct = product.find_one({'url': producturl})
                # tempproduct = False
                if not tempproduct:
                    # msg += u"Product used: " + tempproduct['name'] + " .Used proxy: " + goog.config['proxy'] + '\n'
                    allproductslinks.append('http://hotline.ua' + producturl)
                # else:
            return allproductslinks

        def addfilterstoproduct(onef):

            toend = int(db.hotsettings.find_one({"name": "toend"})['value'])

            # assert False, toend
            toend -= 1
            db.hotsettings.update({"name": "toend"}, {'name': 'toend', 'value': toend})

            # filterspagedokonca -= 1
            # filterspagecount = len()
            self.stdout.write("To end:" + str(toend))
            goog = scanhot(onef['href'])
            # itemscount = float(goog.doc.pyquery('h2.selected-filtrs.grey-6')[0].text.split(' ')[1].strip())
            # pages = int(math.ceil(itemscount/24))
            productlinks = goog.doc.pyquery('.cell.gd b.m_r-10 > a.g_statistic')

            # if goog.doc.pyquery('.g-recaptcha').eq(0):
            #     finished = False

            for productlink in productlinks:
                producturl = productlink.attrib['href']
                # self.stdout.write(producturl)

                item = product.find_one({'url': producturl})
                if item:
                    if not 'filters' in item:
                        item['filters'] = []

                    if not onef['filter'] in item['filters']:
                        item['filters'].append(onef['filter'])

                    product.update({'url': producturl}, item)
                # else:
                #     error += "Not Found: " + producturl + ", " + onef['href'] + "\n"

        # with Profiler() as p:

        #     urls = [
        #         'http://www.python.org',
        #         'http://www.python.org/about/',
        #         'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
        #         'http://www.python.org/doc/',
        #         'http://www.python.org/download/',
        #         'http://www.python.org/getit/',
        #         'http://www.python.org/community/',
        #         'https://wiki.python.org/moin/',
        #         'http://planet.python.org/',
        #         'https://wiki.python.org/moin/LocalUserGroups',
        #         'http://www.python.org/psf/',
        #         'http://docs.python.org/devguide/',
        #         'http://www.python.org/community/awards/'
        #         # etc..
        #         ]

        #     # Make the Pool of workers
        #     pool = ThreadPool(1)

        #     # Open the urls in their own threads
        #     # and return the results
        #     results = pool.map(urllib2.urlopen, urls)

        #     #close the pool and wait for the work to finish
        #     pool.close()
        #     pool.join()

        allproductslinks = []
        filterspagedokonca = 0
        filterdb = db.hotfilters
        filteritemdb = db.hotfiltersitems
        category = db.hotcategory
        product = db.hotproduct
        propertydb = db.hotproperty
        settingdb = db.hotsettings
        allproductslinks = []

        if settingdb.find_one({'name': 'status'}):
            settingdb.update({'name': "status"}, {"value": "started", "name": "status"})
        else:
            settingdb.insert_one({"value": "started", "name": "status"})

        product.remove({"name": ""})

        self.stdout.write(args[0])

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
        filterpages = []


        goog = Grab(log_file='/tmp/log.html')
        goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
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


        settingdb.insert_one({"value": categoryname, "name": "status"})

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


                            try:
                                string = tostring(fitem)
                                m = re.search(r"\(([0-9_]+)\)", string)
                                fitems =  float(m.group(1))
                                # itemscount = float(goog.doc.pyquery('h2.selected-filtrs.grey-6')[0].text.split(' ')[1].strip())
                                fpages = int(math.ceil(items/24))
                            except Exception, e:
                                fpages = 1
                                fitems = 1

                                # raise e                            string = tostring(fitem)

                            fitext = fitem.text.strip()
                            href = fitem.attrib['href']
                            fid = int(href.split('/')[3])
                            filteritem = filteritemdb.remove({'href': href})
                            # if not filteritem:
                            filteriteminserted = filteritemdb.insert_one({'name': fitext, 'href': href, 'hid': fid, 'filter': ObjectId(filterinserted_id), 'items': fitems, 'pages': fpages, 'finished': False})

                            for fi in range(0, pages):
                                filterpages.append({"href": "http://hotline.ua" + href + "?p=" + str(fi), "filter": fid})
            i+=1

        # for fp in filterpages:
        #     self.stdout.write(fp)

        # assert False, len(filterpages)

        # return

        pageurls = []

        # for i in range(0, pages):

        #     pageurl = "http://hotline.ua" + url + "?p=" + str(i)
        #     pageurls.append(pageurl)
            # self.stdout.write('Page now: ' + str(i))

            # settingdb.update({'name': "status"}, {"value": "Category: " + categoryname + ". Scanning product page:" + str(i) + " From:" + str(pages), "name": "status"})

        # assert False, pageurls
        # with Profiler() as p:
        #     pool = ThreadPool(14)

        #     allpagesurls = len(pageurls)

        #     allproductslinkslist = pool.map(getproductsurl, pageurls)

        #     pool.close()
        #     pool.join()

        # allproductslinks = []

        # for alll in allproductslinkslist:
        #     allproductslinks += alll

        # # assert False, allproductslinkslist[0]

        # self.stdout.write(str(len(allproductslinks)))

        #     # goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
        # # with Profiler() as p:
        #     # Make the Pool of workers
        # with Profiler() as p:
        #     pool = ThreadPool(14)

        #     # Open the urls in their own threads
        #     # and return the results
        #     allproductresults = pool.map(get_hotline_data2, allproductslinks)

        #     #close the pool and wait for the work to finish
        #     pool.close()
        #     pool.join()

        # self.stdout.write(str(len(allproductresults)))

        # for productitem in allproductresults:
        #     productitem['category'] = ObjectId(cat_id)
        #     product.insert_one(productitem)

        # with Profiler() as p:

        #     pool = ThreadPool(14)

        #     filterspagecount = len(filterpages)

        #     if db.hotsettings.find_one({'name': 'toend'}):
        #         db.hotsettings.update({'name': 'toend'}, {'name': 'toend', 'value': filterspagecount})
        #         # assert False, "we are zdes"
        #     else:
        #         db.hotsettings.insert_one({'name': 'toend', 'value': filterspagecount})
        #         # assert False, "we are tut"/

        #     pool.map(addfilterstoproduct, filterpages)

        #     pool.close()
        #     pool.join()

        products = list(product.find({'category': ObjectId(cat_id)}))
        productscount =len(products)

        with Profiler() as p:
            for oneproduct in products:

                productscount -= 1
                self.stdout.write('To end: ' + str(productscount))
                for prop in oneproduct['properties']:
                    propname = prop['name']
                    # self.stdout.write(propname)
                    if not propertydb.find_one({'name': propname, 'category': ObjectId(cat_id)}):
                        propertydb.insert_one({'name': propname, 'category': ObjectId(cat_id)})


        productscount = len(products)

        with Profiler() as p:
            for one in products:
                productscount -= 1
                self.stdout.write('To end: ' + str(productscount))
                for prop in one['properties']:
                    if prop['name'] == u"Производитель":
                        self.stdout.write(prop['prop'])
                        one['brand'] = prop['prop']
                        product.update({'_id': ObjectId(one['_id'])}, one)

