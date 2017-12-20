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
            p.colors = None
            p.save()
            print p.pk


