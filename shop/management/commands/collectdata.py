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
            items = []
            if p.category:
                items.append(p.category.name)
            if p.brand:
                items.append(p.brand.name)

            items.append(p.name)

            # if p.properties:
            #     for pro in p.properties:
            #         items.append(pro[1])
            #         items.append(pro[2])

            p.search = " ".join(items)
            p.save()

            print p.pk
