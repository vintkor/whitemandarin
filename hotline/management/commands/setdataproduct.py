# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Poll
from grab import Grab
import re
import urllib
import datetime
import json
from shop.models import *
# from hotline.models import *
# from .models import *
import time
import urllib
import random
from discount.settings import *
# from hotline.utils import *
from pyquery import PyQuery as pq
import codecs
from django.db.models import Q
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient()
db = client.hotline

# from hotline.utils import *
import math

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('url')


    def handle(self, *args, **options):
        filterdb = db.hotfilters
        filteritemdb = db.hotfiltersitems
        category = db.hotcategory
        hotproductdb = db.hotproduct
        propertydb = db.hotproperty
        items = []
        url = options['url']
        allfilters = []
        cat_id = category.find_one({'url': url})['_id']

        # products = list(product.find({'category': ObjectId(cat_id)}))

        sitecategories = Category.objects.filter(hotlineurl=url)

        # assert False, sitecategories

        for sitecategory in sitecategories:
            # sitecategory.clearfiltersprops()
            coloritems = ColorProduct.objects.filter(product__category=sitecategory, href__isnull=False)
            for color in coloritems:
                hotproduct = hotproductdb.find_one({"url": color.href})
                if hotproduct:
                    self.stdout.write(hotproduct['url'])
                    product = color.product

                    items = []

                    # color = ncolor
                    # assert False, enumerate(hotfilters)
                    cat = color.product.category
                    catfilters = cat.filters.all()

                    catfiltersids = []

                    for catf in catfilters:
                        catfiltersids.append(catf.id)

                    items = []
                    filters = []
                    properties = []

                    if 'filters' in hotproduct:
                        for onef in hotproduct['filters']:
                            fi = db.hotfiltersitems.find_one({'hid': onef})
                            mainf = db.hotfilters.find_one({'_id': ObjectId(fi['filter'])})
                            items.append({
                                'name': mainf['name'],
                                'value': fi['name'],
                                })

                            oitems = FilterSelect.objects.filter(value=mainf['name'], filter__name=mainf['name'])

                            for o in oitems:
                                if o.filter.id in catfiltersids:
                                    filters.append(o.id)





                    for allf in cat.filters.all():
                        for item in items:
                            if allf.name == item['name']:
                                for selfi in allf.items:
                                    if selfi.value == item['value']:
                                        filters.append(selfi.id)


                    for allp in cat.properties.all().order_by('ordering'):
                        for oneprop in hotproduct['properties']:
                            if allp.name == oneprop['name']:
                                properties.append([allp.id, allp.name, oneprop['prop']])

                # start = datetime.datetime.strptime(options['start'], '%d.%m.%Y')
                    product.filters = filters
                    product.properties = properties

                    product.save()


        send_mail(u'Закончена категория - ' + sitecategories[0].name, sitecategories[0].name, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)