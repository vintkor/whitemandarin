# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from slugify import slugify
from grab import Grab
from django.conf import settings

import urllib

class Command(BaseCommand):

    def handle(self, *args, **options):

        products = Product.objects.all()
        for p in products:

            if not p.filters:

                f = []
                filters = FilterItem.objects.filter(product=p)
                for fil in filters:
                  f.append(int(fil.value))

                p.filters = f

                if p.category:
                    properties = []
                    print p.id

                    allprops = p.category.properties.all().order_by('ordering')

                    for allp in allprops:
                        pro = PropertyProduct.objects.filter(product=p, property=allp)
                        if pro:
                            pro = pro[0]
                            properties.append([pro.property.id, pro.property.name, pro.value])

                    # props = PropertyProduct.objects.filter(product=p)
                    # for pro in props:
                    #     if pro in allprops:
                    #         allprops.remove(pro.property)

                    # for p in allprops:
                    #     properties.append([p.id, p.name, ""])

                    if properties:
                        p.properties = properties
                        p.save()
                # p.save()
