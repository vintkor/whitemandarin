# -*- coding: utf-8 -*-
from grab import Grab
from pyquery import PyQuery as pq
import json
import os
from cms.local_settings import PROJECT_PATH
import re
from shop.models import *
import time

def scanhot(pageurl):

    proxy = Proxy.objects.filter(banned=False).order_by('?')

    if proxy:
        proxy = proxy[0]

    else:
        time.sleep(60)
        return scanhot(pageurl)

    goog = Grab(timeout=30)
    goog.setup(proxy=proxy.hostport, proxy_userpwd=proxy.userpass)
    goog.go(pageurl)

    if goog.doc.pyquery('.g-recaptcha').eq(0):
        proxy.banned = True
        proxy.save()
        return scanhot(pageurl)

    return goog


def get_hotline_data2(sresult):
    # g = Grab(timeout=30)
    # g.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
    # g.go(sresult)

    g = scanhot(sresult)

    pitems = g.pyquery('div#gallery-box > a')

    # import codecs

    # file = codecs.open(PROJECT_PATH + '/../6.txt', "w", "utf-8")
    # file.write(g.response.unicode_body())
    # file.close()

    images = []
    videosresults = []
    mainproperties = []
    advensedroperties = []

    # assert False, pitems.length
    for pitem in pitems:
        images.append(pitem.attrib['href'])
        # self.stdout.write()

    videos = g.pyquery('img.ico.g_statistic')

    for pitem in videos:
        videosresults.append(pitem.attrib['data-hl_gallery_video_hash'])
        # self.stdout.write(pitem.attrib['data-hl_gallery_video_hash'])
    # assert False, videos.length

    prophtml = pq(g.response.unicode_body())
    properties = prophtml('table#full-props-list > tr')
    mproperties = prophtml('div#short-props-list > table > tr')
    # assert False, len(properties)
    try:
        name = prophtml('h1.title-24.p_b-5').outer_html()
        name = re.sub(r'<[^>]*?>', '', name).strip()
        name = re.sub("^\s+|\n|\r|\s+$", '', name)
        hotline_name = re.sub(r'\s+', ' ', name).replace('"', '')
    except:
        hotline_name = ""
    hotline = sresult.split('hotline.ua')[1]

    try:
        price = prophtml('a.range-price.orng strong')[0].text.split(u' – ')
        price_min = int(price[0].replace(' ','').replace(u'\xa0', ''))
        price_max = int(price[1].replace(' ','').replace(u'\xa0', ''))
    except:
        price_min = 0
        price_max = 0
    # price_max = re.sub(r'\s+', ' ', price_max)

    # assert False, price_max

    # file = codecs.open(PROJECT_ROOT + '/static/test2.txt', "w", "utf-8")
    # file.write(price_max)
    # file.close()
    # assert False, price





    for prop in properties:
        prop_pq = pq(prop)
        try:
            name = prop_pq('th').outer_html()
            name = re.sub(r'<[^>]*?>', '', name).strip().replace('"', '')
            prop_new = prop_pq('td').outer_html()
            prop_new = re.sub(r'<[^>]*?>', '', prop_new).strip().replace('"', '')
            advensedroperties.append({'name': name, 'prop': prop_new})
        except:
            pass


    for prop in properties:
        try:
            prop_pq = pq(prop)
            name = prop_pq('th').outer_html()
            name = re.sub(r'<[^>]*?>', '', name).strip().replace('"', '')
            prop_new = prop_pq('td').outer_html()
            prop_new = re.sub(r'<[^>]*?>', '', prop_new).strip().replace('"', '')
            mainproperties.append({'name': name, 'prop': prop_new})
        except:
            pass

    return {
    'url': hotline,
    'name': hotline_name,
    'photos': images,
    'videos': videosresults,
    'properties': advensedroperties,
    'price_min': price_min,
    'price_max': price_max, }


def get_hotline_data(sresult, ppitem=False, save=True):
    # g = Grab(timeout=30)
    # g.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
    # g.go(sresult)

    g = scanhot(sresult)

    pitems = g.pyquery('div#gallery-box > a')

    # import codecs

    # file = codecs.open(PROJECT_PATH + '/../6.txt', "w", "utf-8")
    # file.write(g.response.unicode_body())
    # file.close()

    images = []
    videosresults = []
    mainproperties = []
    advensedroperties = []

    # assert False, pitems.length
    for pitem in pitems:
        images.append(pitem.attrib['href'])
        # self.stdout.write()

    videos = g.pyquery('img.ico.g_statistic')

    for pitem in videos:
        videosresults.append(pitem.attrib['data-hl_gallery_video_hash'])
        # self.stdout.write(pitem.attrib['data-hl_gallery_video_hash'])
    # assert False, videos.length

    prophtml = pq(g.response.unicode_body())
    properties = prophtml('table#full-props-list > tr')
    mproperties = prophtml('div#short-props-list > table > tr')
    # assert False, len(properties)
    try:
        name = prophtml('h1.title-24.p_b-5').outer_html()
        name = re.sub(r'<[^>]*?>', '', name).strip()
        name = re.sub("^\s+|\n|\r|\s+$", '', name)
        hotline_name = re.sub(r'\s+', ' ', name).replace('"', '')
    except:
        hotline_name = ""
    hotline = sresult.split('hotline.ua')[1]

    try:
        price = prophtml('a.range-price.orng strong')[0].text.split(u' – ')
        price_min = int(price[0].replace(' ','').replace(u'\xa0', ''))
        price_max = int(price[1].replace(' ','').replace(u'\xa0', ''))
    except:
        price_min = 0
        price_max = 0
    # price_max = re.sub(r'\s+', ' ', price_max)

    # assert False, price_max

    # file = codecs.open(PROJECT_ROOT + '/static/test2.txt', "w", "utf-8")
    # file.write(price_max)
    # file.close()
    # assert False, price





    for prop in properties:
        prop_pq = pq(prop)
        try:
            name = prop_pq('th').outer_html()
            name = re.sub(r'<[^>]*?>', '', name).strip().replace('"', '')
            prop_new = prop_pq('td').outer_html()
            prop_new = re.sub(r'<[^>]*?>', '', prop_new).strip().replace('"', '')
            advensedroperties.append({'name': name, 'prop': prop_new})
        except:
            pass


    for prop in properties:
        try:
            prop_pq = pq(prop)
            name = prop_pq('th').outer_html()
            name = re.sub(r'<[^>]*?>', '', name).strip().replace('"', '')
            prop_new = prop_pq('td').outer_html()
            prop_new = re.sub(r'<[^>]*?>', '', prop_new).strip().replace('"', '')
            mainproperties.append({'name': name, 'prop': prop_new})
        except:
            pass

    if save:
    # self.stdout.write(hotline)
        ppitem.hotline = hotline
        ppitem.hotline_name = hotline_name
        ppitem.hotline_photos = json.dumps(images)
        ppitem.hotline_videos = json.dumps(videosresults)
        ppitem.hotline_mainfilters = json.dumps(mainproperties)
        ppitem.hotline_filters = json.dumps(advensedroperties)
        ppitem.hotline_price_min = price_min
        ppitem.hotline_price_max = price_max
        ppitem.save()

    else:

        return {
        'url': hotline,
        'name': hotline_name,
        'photos': images,
        'videos': videosresults,
        'properties': advensedroperties,
        'price_min': price_min,
        'price_max': price_max, }
