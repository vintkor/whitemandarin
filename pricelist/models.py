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
import json
import copy

from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

DROPBOX = (('-', '-'),)



class Currency(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=250, blank=True, default="")
    price = models.DecimalField(verbose_name="Курс", default=0, blank=True, null=True, max_digits=7, decimal_places=2)



    def __unicode__(self):
        return self.name + ' ' + str(self.price)

    class Meta:
        verbose_name_plural = "Курсы валют"
        verbose_name = "Курс валют"


class Provider(models.Model):

    name = models.CharField(verbose_name=u'Название', max_length=250, blank=True, default="")
    info = models.TextField(verbose_name=u"Информация", blank=True, null=True, default="")
    block = models.BooleanField(default=False, verbose_name=u'Заблокировано')
    # dropbox_dir =  models.CharField(verbose_name=u'Название', max_length=250, blank=True, default="", choices=DROPBOX)
    path = models.CharField(verbose_name=u'Путь к папке с прайсами в дропбоксе', max_length=250, blank=True, default="")
    official = models.BooleanField(default=False, verbose_name=u'Официал')
    rrc = models.BooleanField(default=False, verbose_name=u'РРЦ')
    garanteemonth = models.IntegerField(verbose_name=u'Гарантия месяцев поставщик', default=0, blank=True)
    discount = models.IntegerField(verbose_name=u'Скидка колонка', default=0, blank=True)
    # nal = models.BooleanField(default=False, verbose_name=u'Наличае')
    # nalrow = models.IntegerField(verbose_name=u'Наличае ряд', default=0, blank=True)
    # nalsym = models.CharField(verbose_name=u'Наличае символ', max_length=250, blank=True, default="")
    @property
    def files(self):
        return FileProvider.objects.filter(provider=self)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Поставщики"
        verbose_name = "Поставщик"


class Settings(models.Model):

    AVAILABILITYTYPE = (
        (0, '='),
        (1, '<>'),
        (2, 'IN')
        )
    currency = models.ForeignKey(Currency, verbose_name='Валюта', blank=True, null=True)
    excellist = models.IntegerField(verbose_name=u'Лист экселя, если 0 значит все или только', default=0, blank=True)

    brand = models.IntegerField(verbose_name=u'Бренд колонка', default=0, blank=True)
    model = models.IntegerField(verbose_name=u'Модель колонка', default=0, blank=True)
    model2 = models.CharField(verbose_name=u'Модель колонка 2', max_length=250, blank=True, default="")
    model3 = models.CharField(verbose_name=u'Модель колонка 3', max_length=250, blank=True, default="")
    articul = models.IntegerField(verbose_name=u'Артикул колонка', default=0, blank=True)
    description = models.IntegerField(verbose_name=u'Описание колонка', default=0, blank=True)
    description2 = models.IntegerField(verbose_name=u'Описание колонка 2', default=0, blank=True)
    description3 = models.IntegerField(verbose_name=u'Описание колонка 3', default=0, blank=True)
    # additionaldescription = models.CharField(verbose_name=u'Дополнительные поля к описпнанию', max_length=250, blank=True, default="")
    garantee = models.IntegerField(verbose_name=u'Гарантия колонка', default=0, blank=True)
    price = models.IntegerField(verbose_name=u'Цена колонка', default=0, blank=True)
    price_rrc = models.IntegerField(verbose_name=u'Цена колонка РРЦ', default=0, blank=True)

    availabilityrow = models.IntegerField(verbose_name=u'Доступность колонка', default=0, blank=True)
    availabilityequal = models.IntegerField(verbose_name=u'Доступность тип', blank=True, default=0, choices=AVAILABILITYTYPE)
    availabilityvalue = models.CharField(verbose_name=u'Доступность значение', max_length=250, blank=True, default="")
    availabilityuse = models.BooleanField(verbose_name='Проверять доступность', default=False)



    class Meta:
        abstract = True
    

class FileProvider(Settings):
    provider = models.ForeignKey(Provider, verbose_name='Поставщик', blank=True, null=True)
    # dropbox_file =  models.CharField(verbose_name=u'Dropbox File', max_length=250, blank=True, default="", choices=DROPBOX)
    path = models.CharField(verbose_name=u'Путь к файлу в дропбоксе', max_length=250, blank=True, default="")
    # sizefile = models.IntegerField(verbose_name=u'Размер файла', default=0, blank=True)
    # upload = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name='Файл')
    uploadtime = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True, verbose_name="Дата последней загрузки")
    content_hash = models.TextField(verbose_name=u"Content Hash", blank=True, null=True) 


class PriceString(models.Model):
    provider = models.ForeignKey(Provider, verbose_name='Поставщик', blank=True, null=True)
    currency = models.ForeignKey(Currency, verbose_name='Валюта')
    # currency = models.CharField(verbose_name=u'Валюта', max_length=250, blank=True)
    
    brand = models.CharField(verbose_name=u'Бренд', max_length=250, blank=True)
    articul = models.CharField(verbose_name=u'Артикул', max_length=250, blank=True)
    model = models.TextField(verbose_name=u"Модель", blank=True, null=True)
    description = models.TextField(verbose_name=u"Описание", blank=True, null=True)
    searchindex = models.TextField(verbose_name=u"Поисковый индекс", blank=True, null=True)
    
    linked = models.BooleanField(verbose_name='Linked', default=False)
    changed = models.BooleanField(verbose_name='Изменено', default=True)

    inproducts = JSONField(verbose_name='Products', blank=True, null=True)
    inhotline = JSONField(verbose_name='Hotline', blank=True, null=True)
    inprice = JSONField(verbose_name='Price', blank=True, null=True)
    
    garantee = models.IntegerField(verbose_name=u'Гарантия', default=0)
    price = models.IntegerField(verbose_name=u'Цена в валюте поставщика', default=0)
    price_grn = models.IntegerField(verbose_name=u'Цена в гривнах', default=0)
    price_grn_rrc = models.IntegerField(verbose_name=u'Цена в гривнах ррц', default=0)
    
    def __unicode__(self):
        return self.provider.name + ' ' + unicode(self.model)

    class Meta:
        verbose_name_plural = "!Строчка прайса"
        verbose_name = "!Строчка прайсов"

    def save(self):
        # assert False, self.price

        self.price_grn = int(round(float(self.price) * float(self.currency.price)))
        self.searchindex = unicode(self.brand) + " " + unicode(self.articul) + " " + unicode(self.model)
        super(PriceString, self).save()


