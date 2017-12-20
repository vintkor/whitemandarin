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



class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        g = Grab(log_dir="/tmp")
        site = "http://20k.com.ua"
        results = ''
# class  FirmHotline(models.Model):
# class  ScanHotline(models.Model):
# class OneHotline(models.Model):
# class ConcurentHotline(models.Model):

        def make_url(url):
            items = url.split('/')
            del items[-2]
            nurl = '/'.join(items)
            g.go(site + nurl)
            if g.response.code == 200:
                return nurl
            else:
                return make_url(nurl)

            # assert False, nurl


        f = open(PROJECT_ROOT + '/static/error.csv', 'r')
        # assert False, f.split('/n')
        for line in f:
            url = line.split(',')[0]
            g.go(url)
            if g.response.code == 404:
                if not '.jpg' in url:
                    l = url.split('http://20k.com.ua')[1]
                    sl = l.split('?')[0]
                    if 'index.php' in l:
                        n = '/'
                    else:
                        n = make_url(sl)

                    results += l + ',' + n + '\n'

                    self.stdout.write(l + ',' + n)

        f = open(PROJECT_ROOT + '/static/results.csv', 'w')
        f.write(results)
        f.close()
