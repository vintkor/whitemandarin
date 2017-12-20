from django.core.management.base import BaseCommand, CommandError
from shop.models import *
from slugify import slugify
import codecs
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        file = codecs.open('price.txt', "r", "utf-8")
        items = json.loads(file.read())
        noitems = ""
        # file.close()
        # assert False, items
        for item in items:
            cs = ColorProduct.objects.filter(idname=item['id'])
            if cs:
                for c in cs:
                    print c.pk
                    c.price = item['price']
                    c.save()
            else:
                noitems += item['id'] + ':' + item['name'] + '\n'

        
        file = codecs.open('noprice.txt', "w", "utf-8")
        file.write(noitems)
        file.close()