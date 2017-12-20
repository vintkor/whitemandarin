# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from content.models import Article
from slugify import slugify
from grab import Grab
from django.conf import settings
import re

import urllib

class Command(BaseCommand):

    def handle(self, *args, **options):

        articles = Article.objects.all()
        for a in articles:
            print a.pk
            a.short_text = re.sub("(<img.*?>)", "", a.short_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            a.full_text = re.sub("(<img.*?>)", "", a.full_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)

            a.save()
