# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from slugify import slugify
from grab import Grab
from django.conf import settings

import urllib
import json
import codecs

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        file = codecs.open('../shop.json', "r", "utf-8")
        items = json.loads(file.read())

        for item in items:
            if item['model'] == 'shop.product':
                # assert False, item['fields']['filters']
                product = Product.objects.filter(pk=item['pk'])
                if product:
                    product = product[0]
                    if product.giftproduct.all() and product.filters==[]:
                        print item['pk']
                        print item['fields']['properties']
                        if 'filters' in item['fields']:
                        #     product = product[0]
                            product.filters = item['fields']['filters']
                            product.properties = item['fields']['properties']
                            product.save()
                            print item['pk']
        # noitems = ""


        # products = Product.objects.all()
        # for p in products:

        #     if not p.filters:

        #         f = []
        #         filters = FilterItem.objects.filter(product=p)
        #         for fil in filters:
        #           f.append(int(fil.value))

        #         p.filters = f

        #         if p.category:
        #             properties = []
        #             print p.id

        #             allprops = p.category.properties.all().order_by('ordering')

        #             for allp in allprops:
        #                 pro = PropertyProduct.objects.filter(product=p, property=allp)
        #                 if pro:
        #                     pro = pro[0]
        #                     properties.append([pro.property.id, pro.property.name, pro.value])

        #             # props = PropertyProduct.objects.filter(product=p)
        #             # for pro in props:
        #             #     if pro in allprops:
        #             #         allprops.remove(pro.property)

        #             # for p in allprops:
        #             #     properties.append([p.id, p.name, ""])

        #             if properties:
        #                 p.properties = properties
        #                 p.save()
        #         # p.save()
