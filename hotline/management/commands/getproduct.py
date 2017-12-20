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
from hotline.utils import *
from pyquery import PyQuery as pq
import codecs

from django.db.models import Q



class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        def decode_captcha(newcaptcha, pitem):
            goog.go("https://ipv4.google.com/sorry/CaptchaRedirect?continue=" + newcaptcha.continueurl + '&id=' + newcaptcha.hiddenid + '&captcha=' + newcaptcha.response )
            if goog.doc.select('//h3[@class="r"]/a').exists():
                # assert False, 'we are here'
                sresult = goog.doc.select('//h3[@class="r"]/a')[0].attr('href')
                get_hotline_data(sresult, pitem)
            else:
                pass

        def wait_enter_captcha(captcha, timer, pitem):
            self.stdout.write('captcha continueurl:' + continueurl)
            newcaptcha = EcomerceCaptcha.objects.filter(pk = captcha.pk).get()
            if newcaptcha.response:
                decode_captcha(newcaptcha, pitem)
            else:
                self.stdout.write('Pause: ' + str(timer))
                time.sleep(timer)
                timer = timer + 5
                wait_enter_captcha(captcha, timer, pitem)


        prefix = 'https://www.google.com.ua/search?q=site:hotline.ua+'
        # assert False, )

        items = PriceString.objects.filter(checked=False)

        for pitem in items:
            if pitem.name:
                goog = Grab(log_file='/tmp/log.html')
                pitem.checked = True
                pitem.save()
                # goog.proxylist.set_source('file', load_file=)

                goog.load_proxylist(os.path.dirname(os.path.realpath(__file__)) + "/proxy.txt", source_type='text_file', proxy_type='http', auto_change=True)
                self.stdout.write(str(pitem.pk))
                words = pitem.name.split(' ')
                searchphrase = '+'.join(words)
                gurl = prefix + searchphrase
                goog.go(prefix + searchphrase)


                # file = codecs.open(PROJECT_ROOT + '/static/test2.txt', "w", "utf-8")
                # file.write(goog.response.body)
                # file.close()

                # assert False, goog.response.body


                if goog.doc.select('//h3[@class="r"]/a').exists():

                    sresult = goog.doc.select('//h3[@class="r"]/a')[0].attr('href')

                    self.stdout.write(sresult)
                    if "?q=" in sresult:
                        sresult = sresult.split('?q=')[1].split('&')[0]
                    self.stdout.write(sresult)
                    get_hotline_data(sresult, pitem)

                else:

                    if (goog.doc.select('//input[@name="id"]').exists()):

                        fname = random.randint(1,110000000)

                        hiddenid = goog.doc.select('//input[@name="id"]')[0].attr('value')
                        continueurl = goog.doc.select('//input[@name="continue"]')[0].attr('value')

                        goog.go("https://ipv4.google.com" + goog.doc.select('//img')[0].attr('src'))

                        f = open(PROJECT_ROOT + '/media/captcha/' + str(fname) + '.jpg', 'w+')
                        f.write(goog.response.body)
                        f.close()

                        captcha = EcomerceCaptcha(request = fname, hiddenid = hiddenid, continueurl = continueurl)
                        captcha.save()

                        wait_enter_captcha(captcha, 5, pitem)


                    # assert False, sresult
