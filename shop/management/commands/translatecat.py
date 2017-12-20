# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from slugify import slugify
from grab import Grab
from django.conf import settings
import urllib
import json 

class Command(BaseCommand):

    def handle(self, *args, **options):

        categories = Category.objects.all()
        for c in categories:
            response = urllib.request.urlopen('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20170411T080638Z.903be6df66103bfd.14c602a948c5744ffa3be40f7c3784293dc1d164&text=' + c.name + '&lang=ru-uk')
            assert False, json.loads(response)
