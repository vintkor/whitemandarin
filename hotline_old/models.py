# -*- coding: utf-8 -*-
from django.db import models
from tinymce import models as tinymce_model
import random
from django.conf import settings
from content.fields import *
from mptt.models import MPTTModel, TreeForeignKey
from profile.models import User
from content.models import Article
from django.core.mail import send_mail, EmailMessage
import datetime
import pickle
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from shop.models import ColorProduct, Category
from django.utils import timezone



def make_upload_path(instance, filename, prefix = False):
    # Переопределение имени загружаемого файла.
    n1 = random.randint(0, 10000)
    n2 = random.randint(0, 10000)
    n3 = random.randint(0, 10000)
    n4 = random.randint(0, 10000)
    n5 = random.randint(0, 10000)
    filename = str(n1)+"_"+str(n2)+"_"+str(n3)+"_"+str(n4)+"_"+str(n5) + '.jpg'
    return u"%s/%s" % (settings.IMAGE_UPLOAD_DIR, filename)


class FirmHotline(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    url = models.CharField(max_length=250, verbose_name="Url")
    itemid = models.IntegerField(verbose_name="itemid", default=0)
    pub_date = models.DateField(default=timezone.now, blank=True, verbose_name="Дата публикации")
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Название фирм"
        verbose_name = "Название фирмы"

class ScanHotline(models.Model):
    pub_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Дата публикации")
    category = models.ForeignKey(Category, verbose_name='Category', null=True, blank=True)
    items = models.IntegerField(verbose_name="items", default=0)
    nowitems = models.IntegerField(verbose_name="items", default=0)
    started = models.BooleanField(verbose_name="Начался", default=False)
    finished = models.BooleanField(verbose_name="Закончен", default=False)
    lastitems = models.IntegerField(verbose_name="lastitems", default=0)
    pause = models.IntegerField(verbose_name="Pause", default=0)

    def getallfirms(self):

        items = ConcurentHotline.objects.filter(one__scan = self).values('firm_id').distinct()
        pk__in = []
        for item in items:
            pk__in.append(item['firm_id'])

        results = FirmHotline.objects.filter(pk__in=pk__in).values('itemid', 'name')
        return results
        # assert False, items


    # def __unicode__(self):
    #     return self.pub_date
    class Meta:
        verbose_name_plural = "Название фирм"
        verbose_name = "Название фирмы"


class OneHotline(models.Model):
    scan = models.ForeignKey(ScanHotline, verbose_name='ScanHotline')
    product = models.ForeignKey(ColorProduct, verbose_name='Product')
    position = models.IntegerField(verbose_name="Position", default=0)
    total = models.IntegerField(verbose_name="Total", default=0)
    max = models.IntegerField(verbose_name="Max", default=0)
    min = models.IntegerField(verbose_name="Min", default=0)
    concurents = models.TextField(verbose_name="Concurents", default='')

    def get_concurents(self):
        items = ConcurentHotline.objects.filter(one=self).order_by("position")
        results = []
        for item in items:
            results.append({
                'concurent_id': item.firm.itemid,
                'name': item.firm.name,
                'position': item.position,
                'price': item.price,
            })
        return results

    def __unicode__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = ""
        verbose_name = ""


class ConcurentHotline(models.Model):
    one = models.ForeignKey(OneHotline, verbose_name='OneHotline')
    firm = models.ForeignKey(FirmHotline, verbose_name='FirmHotline')
    position = models.IntegerField(verbose_name="position", default=0)
    price = models.IntegerField(verbose_name="price", default=0)

    class Meta:
        verbose_name_plural = ""
        verbose_name = ""
