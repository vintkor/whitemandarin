# -*- coding: utf-8 -*-
import turbosmsua

from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Template
from django.utils.html import strip_tags
from shop.models import *
from slugify import slugify
from grab import Grab

class Command(BaseCommand):

    def handle(self, *args, **options):
        items = Product.objects.all()

        for item in items:

            print str(item.pk)
            search = []
            search.append(item.name)
            if item.idcode:
                search.append(item.idcode)
            if item.category:
                search.append(item.category.name)

            if item.brand:
                search.append(item.brand.name)

            if item.category:
                search.append(item.category.name)


            if item.search:
                search.append(item.search)

            if item.text:
                search.append(strip_tags(item.text))

            filters = FilterItem.objects.filter(id__in=item.filters)

            for f in filters:
                search.append(f.filter.name + " " + f.name)

            item.search_text = " ".join(search)
            item.save()
