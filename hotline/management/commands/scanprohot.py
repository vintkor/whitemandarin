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
        items = []
        url = "/mobile/umnye-chasy-smartwatch/"

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
