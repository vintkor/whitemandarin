# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Poll
from grab import Grab
import re
import urllib
import datetime
import json
from shop.models import *
from hotline.models import *
# from .models import *
import time
import urllib
import random
from cms.settings import *
from hotline.utils import *
from pyquery import PyQuery as pq
import codecs
from cms.local_settings import PROJECT_PATH
from django.db.models import Q
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient()
db = client.hotline
from hotline.utils import *
import math




class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        msg = ""

        goog = Grab(log_file='/tmp/log.html')
        goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
        goog = scanhot("http://hotline.ua/catalog/")
        pquery = pq(goog.response.body)

        cells = pquery('.all-cat.m_t-30 li > a')

        # assert False, len(cells)

        # assert False, cells[0].outerHtml()

        # items = []

        for col in cells:
            item = {}
            msg += "python manage.py scanhotall " + col.attrib['href'] + "\n"

        import codecs
        with codecs.open(PROJECT_PATH + '/../bigname.txt', "w", encoding="utf-8") as f:
            f.write(unicode(msg))

            # assert False, col

    # thid action
