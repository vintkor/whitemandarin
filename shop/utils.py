# -*- coding: utf-8 -*-
from grab import Grab
import re
import random
import datetime
import copy
from .models import *
# from cms.local_settings import PROJECT_PATH
# import xmltodict
# import urllib
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

fields = ['title', 'description', 'h1now', 'h1end', 'text']

def generate(text):
    regex = re.findall(u"{(.*?)}", text)
    for r in regex:
        ritems = r.split(',')
        index = random.randint(0, len(ritems) -1)

        replace = ritems[index].strip()

        text = text.replace("{" + r + "}", replace)

    return text



    # get items

    # split items

    # get random

    # replace

def createitem(item, settings):
    checkitems = copy.copy(settings)
    resultitems = copy.copy(settings)
    resultitems['category_setting'] = item

    if not 'categories' in checkitems:
        checkitems['categories__isnull'] = True

    if not 'cities' in checkitems:
        checkitems['cities__isnull'] = True

    if not 'brands' in checkitems:
        checkitems['brands__isnull'] = True

    if not 'providers' in checkitems:
        checkitems['providers__isnull'] = True

    if not 'filters' in checkitems:
        checkitems['filters__isnull'] = True

    for f in fields:
        text = getattr(item, f)
        for key, value in settings.iteritems():
            text = text.replace("{" + key + ".name}", value.name)
            regex = re.findall(u"{" + key + "\.name\|(.*?)}", text)
            for r in regex:
                if int(r) == 1:
                    padeg = "gent"
                if int(r) == 2:
                    padeg = "datv"
                if int(r) == 3:
                    padeg = "accs"
                if int(r) == 4:
                    padeg = "ablt"
                if int(r) == 5:
                    padeg = "loct"
                if int(r) == 6:
                    padeg = "voct"
                if int(r) == 7:
                    padeg = "gen1"
                if int(r) == 8:
                    padeg = "gen2"
                if int(r) == 9:
                    padeg = "acc2"
                if int(r) == 10:
                    padeg = "loc1"
                if int(r) == 11:
                    padeg = "loc2"
                name = value.name.split('(')[0].strip()
                name_r = []

                # assert False, {'name': name}

                namearray = name.split(' ')
                for one in namearray:
                    c = morph.parse(one)[0]
                    try:
                        name_r.append(c.inflect({padeg})[0])
                    except:
                        pass

                name_in = u' '.join(name_r)
                if key == "cities":
                    name_in = name_in.capitalize()

                text = text.replace("{" + key + ".name|" + r + "}", name_in)

        text = generate(text)
        resultitems[f] = text

    item = CategoryText.objects.filter(**checkitems)

    if item:
        print str(item[0].pk)
        CategoryText.objects.filter(pk=item[0].pk).update(**resultitems)
    else:
        print 'new item'
        CategoryText(**resultitems).save()



        # assert False, [text]
        # for settings
# repalce variable
# recalculate item
# save or cretenew


def makeslugify(name, modelname):
    from slugify import slugify
    slug = slugify(name)

    namedclass = {'City': City}

    if namedclass[modelname].objects.filter(slug = slug).exists():
        slug += str(random.randint(0, 10000000))

    return slug

def createsettings(sitems, titems):
    if sitems:
        if 'children' in sitems:
            if not 'children' in sitems['children']:
                sitems['children']['children'] = titems
        else:
            sitems['children'] = titems
    else:
        sitems = titems

    return sitems


