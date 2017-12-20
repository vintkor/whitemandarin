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
        g = Grab(log_dir="/tmp", timeout=30)
        site = "http://20k.com.ua/20k.xml"

        g.go(site)

        items = xmltodict.parse(g.response.body)


        erorrs = ""
        for item in items['urlset']['url']:

            g.go(item['loc'])
            if g.response.status != 200:
                erorrs += "URL: " + item['loc'] + ', Status: ' + str(g.response.status) + '\n'
                # erorrs.append(item['loc'])
                self.stdout.write(item['loc'])


        f = open(PROJECT_ROOT + '/static/res.json', 'w')
        f.write(erorrs)
        f.close()


        # root = etree.fromstring(str(g.response.body))

        # assert False, root.findall('.//urlset')

        # assert False, etree.tostring(root)
        # items = g.pyquery('url loc')

        # for country in root.findall('country'):
# ...÷
        # for item in root.findall('url'):
        #     assert False, item
