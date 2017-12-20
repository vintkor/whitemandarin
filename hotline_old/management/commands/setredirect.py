# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Poll
from grab import Grab
import re
import urllib
import datetime
from shop.models import *
from hotline.models import *
from django.contrib.redirects.models import *
# from .models import *
import time
import urllib
import random
from cms.settings import *
from pyquery import PyQuery as pq



class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        f = open(PROJECT_ROOT + '/static/results.csv', 'r')
        # assert False, f.split('/n')
        for line in f:
            url = line.split(',')
            redirects = Redirect.objects.filter(old_path=url[0])
            if not redirects:
                self.stdout.write(line)
                redirect = Redirect(site_id=1, old_path=url[0], new_path=url[1])
                redirect.save()

        items = Redirect.objects.all()

        for item in items:
            item.old_path = item.old_path.strip()
            item.new_path = item.new_path.strip()
            item.save()
