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
# class  FirmHotline(models.Model):
# class  ScanHotline(models.Model):
# class OneHotline(models.Model):
# class ConcurentHotline(models.Model):

        def scancategories(categories):
            for cat in categories:
                if cat.is_child():
                    # assert False, cat.is_child()
                    scancategories(cat.get_children())
                else:
                    scancategory(cat)


        def scancategory(category):

            scan = ScanHotline(pub_date=datetime.datetime.now(), category=category)
            scan.save()

            # get all active products
            items = ColorProduct.objects.filter(price__gt=0, product__category=category)

            # assert False, len(items)


            g = Grab(log_file='/tmp/log.html', timeout=30)
            # g.load_proxylist(proxy_file='/tmp/proxy.txt', proxy_type='http')

            prefix = 'http://hotline.ua/sr/?tab=pr&sort=1&q='

            myfirmid = 22242

            # titems = []
            import re
            for item in items:
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
                g.go(gurl)

                oneposition = OneHotline(product=item, scan=scan)
                oneposition.save()

                if g.response.code == 200:
                    searchurl(g, item, scan, oneposition)
                # else:
                    # assert False, item
        # get url by item
            # assert False, titems
        # get firms
        def get_mag(link):
            idmag = link.split('/')

            # assert False, idmag

            firm = FirmHotline.objects.filter(itemid=int(idmag[2]))
            if firm:

                self.stdout.write("Firm exists:" + firm[0].name)
                return firm[0]
            else:
                fg = Grab(log_dir="/tmp", timeout=30)
                fg.go('http://hotline.ua' + link)
                body = fg.response.unicode_body()
                pyquery = pq(body)
                name = pyquery('ul.shop-title > li > h1').text()
                try:
                    link = pyquery('ul.info-shops > li > p > a')[0].attrib['href']
                except:
                    link = ""

                firm = FirmHotline(itemid=int(idmag[2]), name=name, url=link)
                firm.save()

                self.stdout.write("New Firm:" + firm.name)
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

            self.stdout.write(href)

            getproduct(href, item, scan, oneposition)

        def getproduct(href, item, scan, oneposition):
            pg = Grab(log_dir="/tmp", timeout=30, referer="http://hotline.ua" + href + 'prices/', headers = {'X-Requested-With'  :  'XMLHttpRequest'})
            purl = "http://hotline.ua" + href + '?tab=2&sort=0'
            pg.go(purl)

            f = open('/Users/a1/Desktop/myfile','w')
            f.write(pg.response.body) # python will convert \n to os.linesep
            f.close() # you can omit in most cases as the destructor will call it

            # self.stdout.write(pg.response.body)

            if item.href != href:
                self.stdout.write('Href reloaded ' + item.name)
                item.href = href
                item.save()

            if pg.response.code == 200:
                # oneposition = OneHotline(product=item, scan=scan)
                # oneposition.save()

                i = 1
                tprice = 0
                positions = pg.pyquery('.new-price-line > div.tx-price.tx-price-line')

                # positions = pg.doc.select('//div[@id="tab2"]/div[@class="tx-price-line tx-price"]')
                # positions = pg.pyquery('#js-top-lines').remove()("div.tx-price-line")
                # positions = pg.pyquery('')
                for pos in positions:
                    onepos = pq(pos)
                    # assert False, onepos

                    maglink = onepos('.logo-box.fl a')[1].attrib['href']
                    self.stdout.write(maglink)
                    # assert False, maglink



                    mag = get_mag(maglink)

                    tprice = str(onepos('a.orng')).split('>')[1].split('&#160;<i')[0]
                    if '&#160;' in tprice:
                        tempprice = tprice.split('&#160;')
                        tprice = tempprice[0] + tempprice[1]

                    if '.' in tprice:
                        tprice = tprice.split('.')[0]

                    tprice = int(tprice)

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

                    self.stdout.write('Product name: ' + item.name + ', Firm Link: ' + maglink + ', Price:' + str(tprice))

                    i += 1

                if tprice:
                    oneposition.max = tprice
                oneposition.total = i
                oneposition.save()


            waittime = random.randint(7,10)
            self.stdout.write('Wait time:' + str(waittime))

            time.sleep(waittime)

        # create ScanHotline

        category_id = 0

        if len(args) > 0:
            category_id = int(args[0])

        # assert False, category_id

        if not category_id:
            categories = Category.objects.filter(level=0).order_by('order')
            scancategories(categories)

        else:
            categories = Category.objects.filter(pk=category_id)
            scancategories(categories)
