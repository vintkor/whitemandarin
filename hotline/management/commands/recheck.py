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

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        items = Proxy.objects.filter(banned=True)
        for item in items:
            item.banned = False
            item.save()
