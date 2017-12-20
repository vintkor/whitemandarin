# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from grab import Grab
import re
import urllib
# import datetime
from shop.models import *
from hotline.models import *
import time
import urllib
import random
from cms.settings import *
from pyquery import PyQuery as pq

from celery.task import periodic_task
from datetime import timedelta

import json
import time
import functools
import httplib
import urllib2

import datetime
from shop.models import *
from cms.local_settings import PROJECT_PATH
import codecs
from django.template import loader, Context
from django.db.models import Q


class BoundHTTPHandler(urllib2.HTTPHandler):

    def __init__(self, source_address=None, debuglevel=0):
        urllib2.HTTPHandler.__init__(self, debuglevel)
        self.http_class = functools.partial(httplib.HTTPConnection,
                source_address=source_address)

    def http_open(self, req):
        return self.do_open(self.http_class, req)


def scancategories(categories):
    for cat in categories:
        if cat.is_child():
            # assert False, cat.is_child()
            scancategories(cat.get_children())
        else:
            scancategory(cat)


def scancategory(scan, now=0):

    # scan = ScanHotline(pub_date=datetime.datetime.now(), category=category)
    # scan.save()
    # get all active products
    items = ColorProduct.objects.filter(price__gt=0, product__category=scan.category, product__published=True)

    scan.started = True
    scan.items = len(items)
    scan.nowitems = now
    scan.save()

    # assert False, len(items)


    g = Grab(log_file='/tmp/log.html', timeout=300)

    g.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
    # g.load_proxylist(proxy_file='/tmp/proxy.txt', proxy_type='http')

    prefix = 'http://hotline.ua/sr/?tab=pr&sort=1&q='

    myfirmid = 22242

    if now:
        items = items[:now-1]

    # titems = []
    # import re
    for item in items:

        scan.nowitems += 1
        scan.lastitems = 0
        scan.pause = 0
        scan.save()
        # if item.name:
            # item.name = 'Alpine SWG-1244 12" (30 см)'
        result = re.sub("[^A-Za-z0-9 ()-]", "", item.productname)
        # titems.append(result)
        # assert False, item.name
        words = result.split(' ')
        searchphrase = '+'.join(words)
        gurl = prefix + searchphrase
        # assert False, item.id
        # assert False, searchphrase

        oneposition = OneHotline(product=item, scan=scan)
        oneposition.save()
        print(123);
        if item.hrefok:
            getproduct(item.href, item, scan, oneposition)
        else:
            print("net")

    scan.finished = True
    scan.pub_date = datetime.datetime.now()
    scan.save()

        # else:
            # assert False, item
# get url by item
    # assert False, titems
# get firms
def get_mag(link):
    idmag = link.split('/')

    firm = FirmHotline.objects.filter(itemid=int(idmag[2]))
    if firm:

        print("Firm exists:" + firm[0].name)
        return firm[0]
    else:
        fg = Grab(log_dir="/tmp", timeout=300)

        fg.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)
        fg.go('http://hotline.ua' + link)
        body = fg.response.body
        pyquery = pq(body)
        name = pyquery('ul.shop-title > li > h1').text()
        try:
            link = pyquery('ul.info-shops > li > p > a')[0].attrib['href']
        except:
            link = ""

        firm = FirmHotline(itemid=int(idmag[2]), name=name, url=link)
        firm.save()

        print("New Firm:" + firm.name)
        return firm

# calculate position
def searchurl(g, item, scan, oneposition):
    # oneposition = OneHotline.object.filter(product=item)

    if item.href and item.hrefok:
        href = item.href
    else:

        pos = g.doc.select('//div[@class="title-box"]/div[@class="ttle"]/link_info/a')
        if pos.exists():
            href = pos[0].attr('href')
            # assert False, href
        else:
            pos = g.doc.select('//a[@class="link_info"]')
            if pos.exists():
                href = pos[0].attr('href')
                # assert False, href
            else:


                # assert False, oneposition
                # assert False, 'we are here'
                return

    print(href)

    getproduct(href, item, scan, oneposition)

def getproduct(href, item, scan, oneposition):
    pg = Grab(log_dir="/tmp", timeout=30)

    # proxy = Proxy.objects.filter(active=True).order_by('?')[0]

    # # proxyaddrlist = proxy.name.split(':')[0:1]
    # # proxyuserlist = proxy.name.split(':')[2:3]

    # proxyaddr = proxy.name.split(':')[0] + ':' + proxy.name.split(':')[1]
    # proxyuser = proxy.name.split(':')[2] + ':' + proxy.name.split(':')[3]

    # print proxyaddr

    # # assert False, proxyuser

    # pg.setup(proxy=proxyaddr, proxy_userpwd=proxyuser, proxy_type="http")

    pg.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy1.txt", source_type='text_file', proxy_type='http', auto_change=True)

    # print pg.config['proxy']

    # pg.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy.txt", source_type='text_file', proxy_type='http', auto_change=True)
    try:
        purl = "http://hotline.ua" + href + 'prices/'
        pg.go(purl)
        # pass
    except Exception, e:
        print "Error: " + purl
        return
        # raise e

    body = pg.response.body
    pyquery = pq(body)
    print('We are here')
    # send_mail('', body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)


    print pg.config['proxy']

    # assert False, pyquery
    try:

        csrf = pyquery('meta[name="csrf-token"]')[0].attrib['content']

    except:
        if pyquery('.g-recaptcha').eq(0):
            print('captcha error')
            # proxy.active=False
            # proxy.save()
            send_mail(pg.config['proxy'], body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
            return


        send_mail('Export error', body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
        csrf = False
        print(csrf)
        print(purl)
        item.hrefok = False
        item.save()

    # send_mail('CSRF', csrf, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)


    if csrf:
        # self.stdout.write(pg.response.body)
        millis = int(round(time.time() * 1000))
        pg.setup(headers = {'X-Requested-With'  :  'XMLHttpRequest', 'X-CSRF-Token': csrf})
        purl = "http://hotline.ua" + href + '?tab=2&sort=0&_=' + str(millis)

        try:
            pg.go(purl)

            # send_mail('Product: ' + item.name, pg.response.body, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)

            # pass
        except Exception, e:
            print "Error: " + purl
            return
            # raise e

        print purl
        # print pg.response.body


        if item.href != href:
            print('Href reloaded ' + item.name)
            item.href = href
            item.save()

        # send_mail('Response code', str(pg.response.code), 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
        if pg.response.code == 200:
            # oneposition = OneHotline(product=item, scan=scan)
            # oneposition.save()

            i = 1
            tprice = 0


            # positions = pg.doc.select('//div[@id="tab2"]/div[@class="tx-price-line tx-price"]')
            # positions = pg.pyquery('div#tab_2 > div.tx-price')
            positions = pg.pyquery('.new-price-line > .price-line-shop.cf')

            # send_mail('Positions', str(len(positions)), 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)


            for pos in positions:
                onepos = pq(pos)
                # maglink = onepos('.rate-shop i a')[0].attrib['href'].replace('reviews/', '')
                maglink = onepos('.m_t-5.cell > a')[0].attrib['href']


                mag = get_mag(maglink)

                # send_mail('Onestr', str(onepos('a.orng.range-price')), 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)

                # return

                # print(str(int(tprice)))
                # time.sleep(10)
                try:

                    tprice = str(onepos('a.orng.range-price')).split('>')[1].split('<')[0].replace(' ', '').replace('&nbsp;', '').replace('&#160;', '')
                    # tprice = str(onepos('a.orng')).split('>')[1].split('&#160;<i')[0]
                    # if '&#160;' in tprice:
                    #     tempprice = tprice.split('&#160;')
                    #     tprice = tempprice[0] + tempprice[1]

                    if '.' in tprice:
                        tprice = tprice.split('.')[0]

                    tprice = int(tprice)

                except:

                    tprice = 0
                if i==1:
                    oneposition.min = tprice

                if mag.itemid == 22242:
                    oneposition.position = i
                # else:
                concrent = ConcurentHotline(one=oneposition, firm=mag, position=i, price=tprice)
                concrent.save()

                # assert False, maglink[0].attrib['href']
                # assert False, str(onepos('a.orng')).split('>')[1].split('&#160;<i')[0]
                # price = onepos('a.orng').split('>')[1].split('&')[0]
                # assert False, tprice.decode('utf-8')

                print('Product name: ' + item.name + ', Firm Link: ' + maglink + ', Price:' + str(tprice))

                i += 1

            if tprice:
                oneposition.max = tprice
            oneposition.total = i
            oneposition.concurents = json.dumps(oneposition.get_concurents())

            oneposition.save()


        # waittime = random.randint(1,2)
        # print('Wait time:' + str(waittime))

        # time.sleep(waittime)


@periodic_task(run_every = timedelta(seconds = 60))
def test():
    print "is works!"

    activescans = ScanHotline.objects.filter(started=True, finished=False)

    querytscans = ScanHotline.objects.filter(started=False)

    if not activescans:

        for one in querytscans:

            scancategory(one)

    else:

        if activescans[0].lastitems == activescans[0].nowitems:


            if activescans[0].pause > 4:


                scancategory(activescans[0], activescans[0].nowitems)

            else:
                activescans[0].pause += 1
                activescans[0].save()

            print activescans[0].pause

        else:

            activescans[0].lastitems = activescans[0].nowitems
            activescans[0].save()



@periodic_task(run_every = timedelta(seconds = 60))
def recalculate():
    kurs = Kurs.objects.get(pk=1)

    if kurs.recount:
        kurs.recount = False
        kurs.save()
        items = ColorProduct.objects.all()

        for item in items:
            print str(item.pk)
            item.recalculate()



@periodic_task(run_every = timedelta(seconds = 60))
def recalculatehotline():
    kurs = Kurs.objects.get(pk=1)

    if kurs.hotline:
        kurs.hotline = False
        kurs.save()

        t = datetime.datetime.now()

        categorys = Category.objects.filter(published=1)

        items = Product.objects.filter(Q(category__hotline=True) | Q(hotline=True), published = True).exclude(brand__slug__isnull=True,category__slug__isnull=True).order_by('category')

        c = items.count()
        template = loader.get_template('shop/hotline_xml.html')

        body_html = template.render(Context({'categorys': categorys, 't': t, 'c': c, 'items': items}))

        file = codecs.open(PROJECT_PATH + '/static/hotline.xml', "w", "utf-8")
        file.write(body_html)
        file.close()

        send_mail('формирование прайса завершено', "формирование прайса завершено", 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)

