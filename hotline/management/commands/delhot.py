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

        # assert False, args[0]
        url = args[0]

        catdata = category.find_one({'url': url})

        cat_id = catdata['_id']

        filters = filterdb.find({'category': ObjectId(cat_id)})

        for f in filters:
            filteritemdb.remove({'filter': ObjectId(f['_id'])})
        product.remove({'category': ObjectId(cat_id)})
        filterdb.remove({'category': ObjectId(cat_id)})
        propertydb.remove({'category': ObjectId(cat_id)})
        category.remove({'_id': ObjectId(cat_id)})
