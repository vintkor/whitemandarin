# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from slugify import slugify
from grab import Grab

import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = Category.objects.all()
        for cat in categories:
            for brand in cat.get_brands:

                # try:
                fseo = FilterSeo.objects.filter(category=cat, brand=brand, fs1__isnull = True, fs2__isnull=True, fs3__isnull=True)
                if not fseo:
                    title = u"Купить " + cat.name + " " + brand.name + u" в Киеве. Цены и отзывы на " + cat.name + " "  + brand.name + u" в Украине - интернет-магазин 20К"

                    filterseo = FilterSeo(category=cat, brand=brand, title=title, h1=cat.name + ' ' + brand.name,
                        slug=brand.slug
                        )
                    filterseo.save()


                    self.stdout.write(cat.name + ' ' + brand.name)

                # except Exception, e:
                #     pass
                #     # raise e
# get all filterseo
            filterseos = FilterSeo.objects.filter(category=cat)

            filterseourls = {}
            for onef in filterseos:
                key = ""
                if onef.brand:
                    key += 'brand_' + str(onef.brand.id)
                if onef.fs1:
                    key += 'prop_' + str(onef.fs1.id)
                if onef.fs2:
                    key += 'prop_' + str(onef.fs2.id)
                if onef.fs3:
                    key += 'prop_' + str(onef.fs3.id)

                filterseourls[key] = onef.slug

            cat.seofilters = json.dumps(filterseourls)
            cat.save()
        g = Grab()
        g.go("https://api.telegram.org/bot316014013:AAHm9q5mhpWUVCmCrYefprNcZvucfosyESQ/sendMessage?chat_id=96941266&text=20k бренды сформированы успешно")
