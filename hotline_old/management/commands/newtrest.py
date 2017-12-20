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
import functools
import httplib
import urllib2

class BoundHTTPHandler(urllib2.HTTPHandler):

    def __init__(self, source_address=None, debuglevel=0):
        urllib2.HTTPHandler.__init__(self, debuglevel)
        self.http_class = functools.partial(httplib.HTTPConnection,
                source_address=source_address)

    def http_open(self, req):
        return self.do_open(self.http_class, req)



class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        handler = BoundHTTPHandler(source_address=("77.123.135.103", 0))
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        response = urllib2.urlopen('http://myip.com.ua')
        body = response.read()
        send_mail('Export error 23445', body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
