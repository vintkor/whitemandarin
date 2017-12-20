# -*- coding: utf-8 -*-
from grab import Grab
from splinter import Browser
from pyquery import PyQuery as pq
import json
import re

from pyvirtualdisplay import Display
from selenium import webdriver



def get_hotline_data(sresult, ppitem):
    display = Display(visible=0, size=(1024, 768))
    display.start()
    with Browser() as browser:
        # Visit URL
        # url = "http://hotline.ua/mobile-mobilnye-telefony-i-smartfony/lenovo-k3-note-k50-t5-blue/"
        browser.visit(sresult)

        html = browser.html
        # url = "http://hotline.ua/mobile-mobilnye-telefony-i-smartfony/lenovo-k3-note-k50-t5-blue/"
        # browser.visit(url)
        pyquery = pq(html)
        # html = browser.html
        # g = Grab(timeout=30)
        # g.go(sresult)
        pitems = pyquery('div#gallery-box > a')

        # assert False, len(pitems)


        images = []
        videosresults = []
        mainproperties = []
        advensedroperties = []

        # assert False, pitems.length
        for pitem in pitems:
            images.append(pitem.attrib['href'])
            # self.stdout.write()

        videos = pyquery('img.ico.g_statistic')

        for pitem in videos:
            videosresults.append(pitem.attrib['data-hl_gallery_video_hash'])
            # self.stdout.write(pitem.attrib['data-hl_gallery_video_hash'])
        # assert False, videos.length

        prophtml = pq(html)
        properties = prophtml('table#full-props-list > tbody > tr')
        mproperties = prophtml('div#short-props-list > table > tr')

        # assert False, len(properties)

        try:
            name = prophtml('h1.title-main').outer_html()
            name = re.sub(r'<[^>]*?>', '', name).strip()
            name = re.sub("^\s+|\n|\r|\s+$", '', name)
            hotline_name = re.sub(r'\s+', ' ', name)
        except:
            hotline_name = ""
        hotline = sresult.split('hotline.ua')[1]

        try:
            price = prophtml('a.range-price.orng strong')[0].text.split(u' – ')
            price_min = price[0].replace(' ','').replace(u'\xa0', '')
            price_max = price[1].replace(' ','').replace(u'\xa0', '')
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
                name = re.sub(r'<[^>]*?>', '', name).strip()
                prop_new = prop_pq('td').outer_html()
                prop_new = re.sub(r'<[^>]*?>', '', prop_new).strip()
                advensedroperties.append({'name': name, 'prop': prop_new})
            except:
                pass


        for prop in properties:
            try:
                prop_pq = pq(prop)
                name = prop_pq('th').outer_html()
                name = re.sub(r'<[^>]*?>', '', name).strip()
                prop_new = prop_pq('td').outer_html()
                prop_new = re.sub(r'<[^>]*?>', '', prop_new).strip()
                mainproperties.append({'name': name, 'prop': prop_new})
            except:
                pass

        # self.stdout.write(hotline)
        ppitem.hotline = hotline
        ppitem.hotline_name = hotline_name
        ppitem.hotline_photos = json.dumps(images)
        ppitem.hotline_videos = json.dumps(videosresults)
        ppitem.hotline_mainfilters = json.dumps(mainproperties)
        ppitem.hotline_filters = json.dumps(advensedroperties)
        ppitem.hotline_price_min = int(price_min)
        ppitem.hotline_price_max = int(price_max)
        ppitem.save()
