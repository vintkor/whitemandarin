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
        items = ColorProduct.objects.filter(price__gt=0, href="")
        # items = ColorProduct.objects,filter(settings)
        prefix = 'https://www.google.com.ua/search?q=site:hotline.ua+'


        # assert False, items
        for pitem in items:
            if pitem.productname:
                goog = Grab(log_file='/tmp/log.html')
                # goog.proxylist.set_source('file', load_file=)

                goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy.txt", source_type='text_file', proxy_type='http', auto_change=True)
                self.stdout.write(str(pitem.pk))
                words = pitem.productname.split(' ')
                searchphrase = '+'.join(words)
                gurl = prefix + searchphrase
                goog.go(prefix + searchphrase)

                # file = codecs.open(PROJECT_ROOT + '/static/test2.txt', "w", "utf-8")
                # file.write(goog.response.body)
                # file.close()

                # assert False, goog.response.body


                if goog.doc.select('//h3[@class="r"]/a').exists():

                    sresult = goog.doc.select('//h3[@class="r"]/a')[0].attr('href')

                    self.stdout.write(sresult)
                    if "?q=" in sresult:
                        sresult = sresult.split('?q=')[1].split('&')[0]

                    sresult = sresult.replace('http://hotline.ua', '')

                    pitem.href = sresult
                    pitem.hrefok = True
                    pitem.save()

                    self.stdout.write(sresult)
                else:
                    self.stdout.write('net')
