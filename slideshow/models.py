# -*- coding: utf-8 -*-
from django.db import models
from tinymce import models as tinymce_model
import random
from django.conf import settings
from content.fields import *
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import to_locale, get_language
import datetime

def make_upload_path(instance, filename, prefix = False):
    # Переопределение имени загружаемого файла.
    n1 = random.randint(0,10000)
    n2 = random.randint(0,10000)
    n3 = random.randint(0,10000)
    filename = str(n1)+"_"+str(n2)+"_"+str(n3) + '.jpg'
    return u"%s/%s" % (settings.IMAGE_UPLOAD_DIR, filename)


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    published = models.BooleanField(verbose_name="Опубликован")
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"


class Slid(models.Model):
    category = models.ForeignKey(Category, verbose_name=u"Категория")
    name = models.CharField(max_length=250, verbose_name="Название")
    link = models.CharField(max_length=250, default="", blank=True,  verbose_name="Ссылка")
    image = models.ImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение")
    text = tinymce_model.HTMLField(blank=True, verbose_name="Содержание RU")
    
    published = models.BooleanField(verbose_name="Опубликован")
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    
        
    def __unicode__(self):
        return self.name
    def pic(self):
        if self.image:
            return u'<img src="%s" width="70"/>' % self.image.url
        else:
            return '(none)'
    pic.short_description = u'Большая картинка'
    pic.allow_tags = True
    class Meta:
        verbose_name_plural = "Слайды"
        verbose_name = "Слайд"