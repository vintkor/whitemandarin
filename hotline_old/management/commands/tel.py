# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Poll
from grab import Grab
import re
import urllib
import datetime
from shop.models import *
from hotline.models import *
# from .models import *
import time
import urllib
import random
from cms.settings import *
from pyquery import PyQuery as pq
from lxml import etree
import xmltodict

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        settings = {
            'price__gt': 0,
            'href': '',
        }
        if args:
            category = Category.objects.get(pk=args[0])
            # assert False, category
            settings['product__category'] = category

        # assert False, settings
        items = ColorProduct.objects.filter(product__category_id__in=[1], price__gt=0)
        # items = ColorProduct.objects,filter(settings)
        prefix = 'https://www.google.com.ua/search?q=site:hotline.ua+'


        # assert False, items
        for pitem in items:
            pitem.hrefok = True
            pitem.save()
