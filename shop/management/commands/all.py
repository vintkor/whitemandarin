# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from slugify import slugify
from grab import Grab
from django.conf import settings

import urllib

class Command(BaseCommand):

    def handle(self, *args, **options):

        products = Product.objects.filter(full_text__icontains="http://")
        for p in products:
            ftext = p.full_text.replace("http://", "https://")
            p.full_text = ftext
            p.save()

            print p.pk
