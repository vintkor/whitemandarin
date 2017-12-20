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
import json
import copy

from redactor.fields import RedactorField
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


def make_upload_path(instance, filename, prefix = False):
    # Переопределение имени загружаемого файла.
    n1 = random.randint(0, 10000)
    n2 = random.randint(0, 10000)
    n3 = random.randint(0, 10000)
    n4 = random.randint(0, 10000)
    n5 = random.randint(0, 10000)
    filename = str(n1)+"_"+str(n2)+"_"+str(n3)+"_"+str(n4)+"_"+str(n5) + '.jpg'
    return u"%s/%s" % (settings.IMAGE_UPLOAD_DIR, filename)

TYPES = (
    # (1, u'Текстовое значение'),
    # (2, u'Числовое значение'),
    (3, u'Выбор фильтра'),
    (4, u'Выбор нескольких фильтров'),
)

WARANTY = (
        (u'Без гарантии', u'Без гарантии'),
        (u'3 месяца', u'3 месяца'),
        (u'6 месяцев', u'6 месяцев'),
        (u'12 месяцев', u'12 месяцев'),
        (u'24 месяца', u'24 месяца'),
    )


class Concurent(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    strong = models.BooleanField(verbose_name="Обязателен", default=False)
    url = models.CharField(max_length=250, verbose_name="Url")
    itemid = models.IntegerField(verbose_name="itemid", default=0)
    pub_date = models.DateField(default=datetime.date.today, blank=True, verbose_name="Дата публикации")
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Название фирм"
        verbose_name = "Название фирмы"


class Filter(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    requery = models.BooleanField(verbose_name="Обязателен", default=False)
    filtertype = models.IntegerField(verbose_name="Название", choices=TYPES, default=1)
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, verbose_name="Урл")
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Фильтр для категории"
        verbose_name = "Фильтры для категорий"


    @property
    def items(self):
        items = FilterSelect.objects.filter(filter = self).order_by('ordering')
        return items

class FilterSelect(models.Model):
    filter = models.ForeignKey(Filter, blank=True, verbose_name="Фильтр")
    value = models.CharField(max_length=250, verbose_name="Значение")
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    slug = models.CharField(max_length=250, db_index=True, default="", blank=True, verbose_name="Урл")
    def __unicode__(self):
        return self.value
    class Meta:
        verbose_name_plural = "Фильтр выбора"
        verbose_name = "Фильтры выборов"

    # def is_active


class Property(models.Model):
    # value = models.CharField(max_length=250, verbose_name=u"Значение")
    name = models.CharField(max_length=250, verbose_name=u"Название")
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Ucat(MPTTModel):
    name = models.CharField(max_length=250, verbose_name="Название")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u"Родительская категория")
    old_id = models.IntegerField(verbose_name="old_id", default=0, blank=True, null=True)
    allfilters = models.TextField(verbose_name=u"Фильтры", blank=True, null=True)
    class Meta:
        verbose_name_plural = "Юг категории"
        verbose_name = "Юг категории"

    def __unicode__(self):
        return self.name

class Uproduct(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    myname = models.CharField(max_length=250, verbose_name="мое название")
    name_rus = models.CharField(max_length=250, verbose_name="Название русское")
    name_ukr = models.CharField(max_length=250, verbose_name="Название украинское")
    category = models.ForeignKey(Ucat, null=True, blank=True, verbose_name=u"Категория")
    articul = models.CharField(max_length=250, verbose_name="Артикул")
    barcode = models.CharField(max_length=250, verbose_name="Баркод")
    brand = models.CharField(max_length=250, verbose_name="Бранд")
    descr = models.TextField(verbose_name=u"Описание", blank=True, null=True)
    guarant = models.CharField(max_length=250,verbose_name=u"Гаранти]", blank=True, null=True)
    old_id = models.IntegerField(verbose_name="old_id", default=0, blank=True, null=True)
    photo = models.CharField(max_length=250, verbose_name=u"Фото", blank=True, null=True)
    url = models.CharField(max_length=250, verbose_name=u"Юрл", blank=True, null=True)
    image = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение")
    rprice_uah = models.IntegerField(verbose_name="Розничная цена", default=0, blank=True, null=True)
    filters = models.TextField(verbose_name=u"Фильтры", blank=True, null=True)


    class Meta:
        verbose_name_plural = "Юг продукт"
        verbose_name = "Юг продукт"

    def __unicode__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=250, verbose_name="Название")
    namebread = models.CharField(max_length=250, verbose_name="Название Бреадкрампс", default="")
    image = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение")
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metakey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metadesc = models.CharField(max_length=250, blank=True, verbose_name="Мета описание")
    slug = models.CharField(max_length=250, blank=True, verbose_name="Урл", unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u"Родительская категория")
    hotline = models.BooleanField(verbose_name="Hotline", default = True)
    nadavi = models.BooleanField(verbose_name="Nadavi", default = True)
    priceua = models.BooleanField(verbose_name="Priceua", default = True)
    published = models.BooleanField(verbose_name="Опубликован", default=False)
    main = models.BooleanField(verbose_name="Выделить", default=False)
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    column = models.IntegerField(verbose_name="Колонка", default=0, blank=True, null=True)
    text = RedactorField(blank=True, verbose_name="Полное описание")
    filters = models.ManyToManyField(Filter, verbose_name=u'Фильтры', blank=True)
    properties = models.ManyToManyField(Property, verbose_name=u'Свойства', blank=True)
    seofilters = models.TextField(verbose_name=u"Сео фильтры", blank=True, null=True)
    allcounts = models.TextField(verbose_name=u"Подсчет данных", blank=True, null=True)
    google_published = models.BooleanField(verbose_name="Google Published", default=False)
    google_price = models.DecimalField(verbose_name="Цена Google в день", default=0, blank=True, null=True, max_digits=7, decimal_places=2)
    imagemenu = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение для главного меню")
    lastscan_date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True, verbose_name="Дата оканчание акции")

    hotlineurl = models.CharField(max_length=250, verbose_name="Hotline url", blank=True, null=True)


    def get_children(self):
        return Category.objects.filter(parent=self).order_by('ordering')

    # @property
    def getcount(self, active_brands, active_filters, one_brand = False, one_filter = False):
        products_args = {'category': self, 'published': True}

        products_args['brand__in'] = []

        # if active_brands:
        #     products_args['brand__in'] = copy.deepcopy(active_brands)

        products_args['pk__in'] = []

        if active_filters:

            i = 0

            for activef in active_filters:

                products_list = []
                products = FilterItem.objects.filter(value=activef).values('product_id')
                for one in products:

                    products_list.append(one['product_id'])

                products_set = set(products_list)

                if i == 0:
                    results_products_set = products_set
                else:
                    # if activef != {'value': '56', 'filter_id': 2L}:
                    #     assert False, results_products_set | products_set
                    results_products_set = results_products_set | products_set


                i += 1

            products_ids = list(results_products_set)

            products_args['pk__in'] = products_ids

        if one_brand and one_brand not in products_args['brand__in']:
            products_args['brand__in'].append(one_brand)

        if one_filter and one_filter not in active_filters:

            products_list = []
            products = FilterItem.objects.filter(value=one_filter).values('product_id')
            for one in products:

                if one['product_id'] not in products_args['pk__in']:
                    products_args['pk__in'].append(one['product_id'])

            # assert False, products_args
        if not products_args['pk__in']:
            del products_args['pk__in']

        if not products_args['brand__in']:
            del products_args['brand__in']

        return Product.objects.filter(**products_args).count()



    @property
    def getseo(self):

        if self.seofilters:
            items = json.loads(self.seofilters)
        else:
            items = {}

        return items


    @property
    def getseofilters(self):
        return FilterSeo.objects.filter(category=self)

    def get_url(self):
        try:
            return '/%s/' % self.slug
        except:
            pass


    def is_child(self):
        if Category.objects.filter(parent=self, published=True):
            return True
        else:
            return False

    @property
    def get_brands(self):
        brands = Product.objects.filter(category = self, published = True).values('brand').distinct()
        # assert False, brands
        brand_ids_in = []

        for brand in brands:
            brand_ids_in.append(brand['brand'])

        result_brands = Brand.objects.filter(pk__in = brand_ids_in, published = True).order_by('name').distinct()
        # assert False, result_brands
        return result_brands

    @property
    def get_products(self):
        return Product.objects.filter(category = self, published = True, price__gt = 0)

    @property
    def get_all_products(self):
        return Product.objects.filter(category = self)

    @property
    def get_childs(self):
        return Category.objects.filter(parent = self, published = True)

    @property
    def get_filters_json(self):
        results = []
        items = self.filters.all()

        for item in items:
            results.append({
                'name' : item.name,
                'value': '',
                })
            for one in item.items:
                results.append({
                    'name' : "--" + one.value,
                    'value': one.pk,
                    })

        return results

    @property
    def get_brands_json(self):
        items = self.get_brands
        results = [{'name':'-----', 'value': '',}]
        for item in items:
            results.append({
                'name': item.name,
                'value': item.pk,
            })

        return results
        # pass
    @property
    def get_colors_json(self):
        items = ColorProduct.objects.filter(product__category=self, price__gt=0)
        results = []
        for item in items:
            results.append({
                'name': item.productname,
                'id': item.pk,
                'brand_id': item.product.brand_id
            })

        return results
        # pass
    def __unicode__(self):
        return self.name

    def childrow(self):
        results = {}
        for i in range(1,6):
            key = "row" + str(i)
            results[key] = Category.objects.filter(parent=self, column=i).order_by("ordering")

        return results

    @property
    def get_complects_json(self):
        items = ComplectItem.objects.filter(product__product__category=self)
        complects = []
        results = []

        for item in items:
            if item.complect not in complects:
                complects.append(item.complect)

        for item in complects:
            results.append({
                'name' : item.name,
                'id'   : item.pk,
            })

        return results

    # hrefok = models.BooleanField(verbose_name="Hotline url OK", default=False)
    def save(self):

        tempcats = Category.objects.filter(pk=self.id)

        if tempcats:
            tempcategory = tempcats.get()

            if tempcategory.hotline != self.hotline:

                for item in self.get_all_products:

                    item.hotline = self.hotline
                    item.save()

            if tempcategory.nadavi != self.nadavi:

                for item in self.get_all_products:

                    item.nadavi = self.nadavi
                    item.save()

            if tempcategory.priceua != self.priceua:

                for item in self.get_all_products:

                    item.priceua = self.priceua
                    item.save()

        super(Category,self).save()

    @property
    def allnames(self):
        names = [self.name]
        items = CategorySinonim.objects.filter(category=self)
        for item in items:
            names.append(item.name)

        return names


    @property
    def sinonim(self):
        sinonims = CategorySinonim.objects.filter(category=self)
        if sinonims:
            sin = sinonims[0].name
        else:
            sin = ''
        return sin



    @property
    def get_all_filters(self):
        results = []
        items = self.filters.all().order_by('name')
        for item in items:
            onedict = {
                'name': item.name,
                'id': item.id,
                'items': [],
            }

            for one in item.items:
                onedict['items'].append({
                    'name': one.value,
                    'id': one.pk,
                    })
            results.append(onedict)
        return results


    @property
    def get_all_properties(self):
        results = []
        items = self.properties.all().order_by('name')
        for item in items:
            results.append({
                'id': item.id,
                'name': item.name,
            })

        return results



    class Meta:
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['name']

# class Waranty

class CategorySinonim(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    category = models.ForeignKey(Category, verbose_name="Категория", null=True, blank = True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Синоним категории"

class Brand(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    image = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение")
    # category = models.ForeignKey(Category, blank=True, verbose_name="Категория")
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    slug = models.CharField(max_length=250, blank=True, verbose_name="Урл", unique=True)
    description = RedactorField(blank=True, verbose_name="Короткое описание")
    full_text = RedactorField(blank=True, verbose_name="Полное описание")
    pub_date = models.DateField(default=datetime.date.today, blank=True, verbose_name="Дата публикации")
    published = models.BooleanField(verbose_name="Опубликован", default=False)
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Бренд"

    def products(self, category):
        items = Product.objects.filter(category = category, brand = self, published = True).order_by('name')
        return items


class FilterSeo(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", null=True, blank = True)
    brand = models.ForeignKey(Brand,  verbose_name="Бренд", null=True, blank=True)
    h1 = models.CharField(max_length=250, verbose_name="Название")
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    text = RedactorField(blank=True, verbose_name="Короткое описание")
    slug = models.CharField(max_length=250, blank=True, verbose_name="Урл")
    fs1 = models.ForeignKey(FilterSelect, verbose_name="FIlter Select 1", related_name='fs1', null=True, blank = True)
    fs2 = models.ForeignKey(FilterSelect, verbose_name="FIlter Select 2", related_name='fs2', null=True, blank = True)
    fs3 = models.ForeignKey(FilterSelect, verbose_name="FIlter Select 3", related_name='fs3', null=True, blank = True)
    active = models.BooleanField(verbose_name="Опубликован", default=True)

    @property
    def get_url(self):
        return '/' + self.category.slug + '/' + self.slug + '/'

    class Meta:
        verbose_name = u'фильтры для сео'
        unique_together = ('category', 'slug',)

    def __unicode__(self):
        return self.title

class ColorRGB(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"Имя")
    rgb = models.CharField(max_length=50, verbose_name=u"RGB", default='#fff')

    def __unicode__(self):
        return '%s' % (self.name)


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    categorysinonim = models.ForeignKey(CategorySinonim, blank=True, null=True, related_name='categorysinonim', verbose_name=u"Синоним категории")
    waranty = models.CharField(max_length=250, verbose_name="Гарантия", choices=WARANTY, default="12 месяцев")
    maincolor = models.CharField(max_length=250, verbose_name="Главный цвет (если нужно)", null=True, blank = True)
    maincolor_id = models.CharField(max_length=250, verbose_name="Главный цвет (id)", null=True, blank = True)
    rgb = models.ForeignKey(ColorRGB, default=1, related_name='product_rgb', verbose_name=u"Цвет RGB")
    idname = models.CharField(max_length=250, verbose_name="Код для 1С", default=0)
    image = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение")
    brand = models.ForeignKey(Brand,  verbose_name="Бренд", null=True)
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    slug = models.CharField(max_length=250, blank=True, verbose_name="Урл", unique=True)
    category = models.ForeignKey(Category, verbose_name="Категория", null=True, blank = True)
    description = RedactorField(blank=True, verbose_name="Короткое описание")
    full_text = RedactorField(blank=True, verbose_name="Полное описание")
    pub_date = models.DateField(default=datetime.date.today, blank=True, verbose_name="Дата публикации")
    published = models.BooleanField(verbose_name="Опубликован", default=False)
    top20 = models.BooleanField(verbose_name="Top20", default=False)
    is_new = models.BooleanField(verbose_name="Новый продукт", default=False)
    action = models.BooleanField(verbose_name="Акция", default = False, blank = True)
    action_time = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True, verbose_name="Дата оканчание акции")
    action_name = models.CharField(max_length=250, verbose_name="Название Акции", null=True, blank = True)
    action_page = models.ForeignKey(Article, verbose_name="Страница Акции", null=True, blank = True)
    newproduct = models.BooleanField(verbose_name="Новинка", default = False)
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    weight = models.IntegerField(verbose_name="Вес используется в поиске", default=0, blank=True, null=True)
    price = models.DecimalField(verbose_name="Цена", default=0, blank=True, null=True, max_digits=7, decimal_places=2)
    oldprice = models.DecimalField(verbose_name="Старая цена", default=0, blank=True, null=True, max_digits=7, decimal_places=2)
    extraproduct = models.ManyToManyField("self", symmetrical=False, verbose_name=u'Дополнительные продукты', related_name = "extra", blank=True)
    giftproduct = models.ManyToManyField("self", symmetrical=False, verbose_name=u'Подарки к продукту', related_name = "gift", blank=True)
    count_views = models.IntegerField(verbose_name=u"Количество просмотров", default=0, blank=True, null=True)
    colors = models.TextField(verbose_name=u"Цвета служебная", blank=True, null=True)
    color_set = models.BooleanField(verbose_name="Главный цвет установлен служебный", default = False)
    hotline = models.BooleanField(verbose_name="Hotline", default = True)
    nadavi = models.BooleanField(verbose_name="Nadavi", default = True)
    priceua = models.BooleanField(verbose_name="Priceua", default = True)
    reit = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Рейтинг", blank=True, null=True, default=0.0)
    count_votes = models.IntegerField(verbose_name="Количество голосов", blank=True, null=True, default=0)
    comments_count = models.IntegerField(verbose_name="Количество коментариев", default=0, blank=True, null=True)
    min_reit = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Минимальная оценка", blank=True, null=True, default=5.0)
    max_reit = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Максимальная оценка", blank=True, null=True, default=0.0)
    has_gift = models.BooleanField(verbose_name="Есть подарок", default = False)

    recomendproduct = models.ManyToManyField("self", symmetrical=False, verbose_name=u'Рекомендоваенные  продукты', related_name = "recomend", blank=True)

    dopcategory = models.ManyToManyField(Category, verbose_name=u'Категории', blank=True, related_name = "dopcategory")

    searchkey = models.TextField(verbose_name=u'Поиск дополнительный', default="", blank=True)
    search = models.TextField(verbose_name=u'Поиск', default="", blank=True)
    ftssearch = models.TextField(verbose_name=u'Поиск индекс', default="", blank=True)

    filters = JSONField(verbose_name='Filters', blank=True, null=True)
    properties = JSONField(verbose_name='Properties', blank=True, null=True)

    @property
    def catsin(self):

        if self.category:
            if self.categorysinonim:
                return self.categorysinonim.name
            else:
                return self.category.sinonim

        return ""



    def save(self):
        try:
            c = self.giftproduct.all().count()
        except:
            c = 0
        if c>0:
            self.has_gift = 1
        else:
            self.has_gift = 0
        super(Product,self).save()

        # maincolor = ColorProduct.objects.filter(product=self, main=True)

        # if maincolor and maincolor[0].price!=self.price:
        #     maincolor[0].price=self.price
        #     maincolor[0].save()
        color = self.maincoloritem

        if color:
            complect_items = ComplectItem.objects.filter(product=color)

            try:
                if complect_items:
                    for one in complect_items:
                        if one.percent and self.price:
                            one.price = round(float(self.price) * float(one.percent) / 100)
                            one.percent = 0
                            one.save()

            except:
                pass
                # else:
                    # one.price = self.price
    @property
    def get_url(self):
        try:
            return '/%s/%s/%s/' % (self.category.slug, self.brand.slug, self.slug)
        except:
            pass

    @property
    def get_properties(self):
        # catproperties = self.category.properties.all().order_by('ordering')
        # items = PropertyProduct.objects.filter(product = self)
        # properties = []

        # allproperties = {}

        # for item in items:
        #     allproperties[item.property.id] = item.value

        # for catprop in catproperties:

        #     id = catprop.id

        #     if id in allproperties:
        #         prop = {'name': catprop.name, 'value': allproperties[id]}
        #     else:
        #         prop = {'name': catprop.name, 'value': "-"}
        #     properties.append(prop)
        # return properties

        results = []
        for prop in self.properties:
            if prop[2]:
                results.append({'name': prop[1], 'value': prop[2]})
            else:
                results.append({'name': prop[1], 'value': '-'})

        return results


    @property
    def get_colors(self):
        try:
            return pickle.loads(self.colors)
        except:
            colors = list(ColorProduct.objects.filter(product = self).exclude(id = self.maincolor_id).order_by('ordering').values())
            colors_result = []
            for item in colors:
                if item['rgb_id']:
                    rgb = ColorRGB.objects.get(id=item['rgb_id']).rgb
                else:
                    rgb = ''
                item['rgb'] = rgb
                item['get_url'] = self.get_url
                # assert False, item
            newproduct = Product.objects.get(pk = self.id)
            newproduct.colors = pickle.dumps(colors)
            newproduct.save()
            return colors

    @property
    def small_image(self):
        import os.path

        if os.path.isfile(settings.PROJECT_ROOT +'/media/' + str(self.image)):
            from easy_thumbnails.files import get_thumbnailer

            thumbnailer = get_thumbnailer(self.image)

            thumbnail_options = {'sharpen': True, 'size': (80, 80)}
            return thumbnailer.get_thumbnail(thumbnail_options)

        else:

            return '/img/no-image-small.jpg'

    @property
    def image2(self):
        import os


        if self.image and os.path.isfile(settings.BASE_DIR +'/discount/media/' + str(self.image)):
            return True

        else:
            return False


    @property
    def complects(self):
        colors = self.product_colors.all()
        items = ComplectItem.objects.filter(product__in = colors)
        # assert False,  items

        results = []

        if items:
            for item in items:
                results.append(item.complect)

        return results

    @property
    def last_comments(self):
        from comments.models import Comments
        # exec "from %s.models import %s" % (paket, item_model)
        # p = eval("%s.objects.get(pk=%d)" % (item_model, int(item_id)))
        nodes = Comments.objects.filter(paket='shop', item_model='Product',item_id=self.id, published=1).order_by('-id')[:3]
        return nodes

    @property
    def maincoloritem(self):
        maincolor = ColorProduct.objects.filter(main=True, product=self)
        if maincolor:
            maincolor = maincolor[0]
        else:
            maincolor = False
        return maincolor

    @property
    def get_photos(self):
        photos = Photo.objects.filter(product=self)
        return photos


    def __unicode__(self):
        return self.name + ' ' + str(self.price)
    class Meta:
        verbose_name_plural = "Продукт"
        ordering = ['name']


class FilterItem(models.Model):
    product = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт", default=0)
    filter = models.ForeignKey(Filter, blank=True, verbose_name=u"Фильтр", default=0)
    value = models.CharField(max_length=250, verbose_name=u'Значение', default='0')
    def __unicode__(self):
        return self.value
    class Meta:
        verbose_name_plural = "Один Фильтр"



class Photo(models.Model):
    name = models.CharField(max_length=250, verbose_name=u"Название")
    image = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name=u"Изображение")
    product = models.ForeignKey(Product, blank=True, related_name='photos', verbose_name=u"Продукт")
    # def save(self):
    #     super(Photo, self).save()
    #     main_color = ColorProduct.objects.get(id = self.product.maincolor_id)
    #     if not main_color.image2:
    #         main_color.image2 = self.image
    #     elif not main_color.image3:
    #         main_color.image3 = self.image
    #     elif not main_color.image4:
    #         main_color.image4 = self.image
    #     elif not main_color.image5:
    #         main_color.image5 = self.image
    #     else:
    #         pass
    #     main_color.save()

class PropertyProduct(models.Model):
    value = models.CharField(max_length=250, verbose_name=u"Значение")
    product = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт")
    property = models.ForeignKey(Property, blank=True, verbose_name=u"Значение")
    def save(self):
        if not self.value and self.id:
            p = PropertyProduct.objects.get(pk=self.id)
            if p.value:
                msg = EmailMessage(u"Удаление свойства", u"Удалено %s - %s " % (self.property.name, self.product.name), u"jcdeesign@gmail.com", [u"webmagic@mail.ua",])
                msg.content_subtype = "html"
                msg.send()
        super(PropertyProduct, self).save()

    def delete(self):
        msg = EmailMessage(u"Удаление свойства", u"Удалено %s - %s " % (self.property.name, self.product.name), u"jcdeesign@gmail.com", [u"webmagic@mail.ua",])
        msg.content_subtype = "html"
        msg.send()
        super(PropertyProduct, self).delete()


class ColorProduct(models.Model):
    product = models.ForeignKey(Product, blank=True, related_name='product_colors', verbose_name=u"Продукт")
    rgb = models.ForeignKey(ColorRGB, default=1, related_name='colors_rgb', verbose_name=u"Цвет RGB")
    name = models.CharField(max_length=250, verbose_name=u"Значение", default='0', blank=True)
    main = models.BooleanField(verbose_name="Main color", default = False)
    price = models.DecimalField(verbose_name="Цена", default=0, blank=True, null=True, max_digits=7, decimal_places=2)
    price_in = models.DecimalField(verbose_name="Цена Входа", default=0, blank=True, null=True, max_digits=7, decimal_places=2)
    oldprice = models.DecimalField(verbose_name="Старая цена", default=0, blank=True, null=True, max_digits=7, decimal_places=2)
    image1 = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение 1")
    image2 = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение 2")
    image3 = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение 3")
    image4 = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение 4")
    image5 = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение 5")
    idname = models.CharField(max_length=250, verbose_name="Код для 1С")
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)
    # slug = models.CharField(max_length=250, blank=True, verbose_name="Урл")
    href = models.CharField(max_length=250, blank=True, verbose_name="Hotline url")
    hrefok = models.BooleanField(verbose_name="Hotline url OK", default=False)

    marga = models.DecimalField(verbose_name="Маржа", default=0, blank=True, null=True, max_digits=11, decimal_places=2)
    margapercent = models.DecimalField(verbose_name="Маржа в процентах", default=0, blank=True, null=True, max_digits=11, decimal_places=2)
 
    price_rrc = models.DecimalField(verbose_name="Цена РРЦ", default=0, blank=True, null=True, max_digits=11, decimal_places=2)
    price_rrc_ok = models.BooleanField(verbose_name="Price rrc OK", default=False)

    lastscan = models.TextField(verbose_name='Lastscan', null=True, blank=True)
    lastscan_date = models.DateTimeField(verbose_name='Lastsscan Date', default=datetime.datetime.now())

    concurents = models.ManyToManyField(Concurent, verbose_name='Конкуренты', null=True, blank=True)

    @property
    def productname(self):
        # import codecs
        # from cms.local_settings import PROJECT_PATH
        name = unicode(self.product.name)
        if self.name:
            name += ' ' + unicode(self.name)
        # f = codecs.open(PROJECT_PATH + '/../test.txt', 'w+', "utf-8")
        # f.write(name)
        # f.close()

        # assert False,name
        return name


    def save(self):
        super(ColorProduct, self).save()

        # assert False, self.product.name

        try:
            self.product.colors = None
            self.product.save()
        except:
            send_mail('Export error', self.product.idname, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
            pass
            # raise e

        default_colors = self.product.product_colors.filter(main = True)
        # assert False, default_colors[1]
        if not default_colors:
            color = self.product.product_colors.all()[0]
            color.main = True
            color.save()
            color.product.image = color.image1
            color.product.price = color.price
            color.product.oldprice = color.oldprice
            color.product.maincolor = color.name
            color.product.idname = color.idname
            color.product.maincolor_id = color.id
            color.product.save()
            photos = self.product.photos.all()
            for photo in photos:
                photo.delete()
            if color.image2:
                photo = Photo(product = color.product, name = color.product.name, image = color.image2)
                photo.save()
            if color.image3:
                photo = Photo(product = color.product, name = color.product.name, image = color.image3)
                photo.save()
            if color.image4:
                photo = Photo(product = color.product, name = color.product.name, image = color.image4)
                photo.save()
            if color.image5:
                photo = Photo(product = color.product, name = color.product.name, image = color.image5)
                photo.save()
        else:
            color = default_colors[0]
            color.product.image = color.image1
            color.product.price = color.price
            color.product.oldprice = color.oldprice
            color.product.maincolor = color.name
            color.product.idname = color.idname
            color.product.maincolor_id = color.id
            try:
                color.product.save()

            except:
                send_mail('Export error', color.idname, 'mozger@ukr.net',['mozger@ukr.net'], fail_silently=False)
                pass
                # raise e
            photos = self.product.photos.all()
            for photo in photos:
                photo.delete()
            if color.image2:
                photo = Photo(product = color.product, name = color.product.name, image = color.image2)
                photo.save()
            if color.image3:
                photo = Photo(product = color.product, name = color.product.name, image = color.image3)
                photo.save()
            if color.image4:
                photo = Photo(product = color.product, name = color.product.name, image = color.image4)
                photo.save()
            if color.image5:
                photo = Photo(product = color.product, name = color.product.name, image = color.image5)
                photo.save()

    def delete(self):
        self.product.colors = None
        self.product.save()
        super(ColorProduct, self).delete()

    def get_url(self):
        try:
            return '/%s/%s/%s/%s/' % (self.product.category.slug, self.product.brand.slug, self.product.slug, self.id)
        except:
            pass



    @property
    def image10(self):
        import os


        if self.image1 and os.path.isfile(settings.BASE_DIR +'/discount/media/' + str(self.image1)):
            return True
        else:
            return False

    @property
    def small_image(self):
        import os.path

        if os.path.isfile(settings.PROJECT_ROOT +'/media/' + str(self.image1)):
            from easy_thumbnails.files import get_thumbnailer

            thumbnailer = get_thumbnailer(self.image1)

            thumbnail_options = {'sharpen': True, 'size': (80, 80)}
            return thumbnailer.get_thumbnail(thumbnail_options)

        else:

            return '/img/no-image-small.jpg'

    def __unicode__(self):
        return '%s %s-%s    %s' % (self.product.name, self.name, self.idname, self.price)

    @property
    def get_name(self):
        return '%s %s' % (self.product.name, self.name)
# class ExtraProduct(models.Model):
#     product_from = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт", related_name="product_from")
#     product_to = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт", related_name="product_to")


class Complect(models.Model):
    name = models.CharField(max_length=250, verbose_name=u'Название')
    # price = models.IntegerField(verbose_name=u'Цена', default=0)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Акционный комплект"

    @property
    def items(self):
        # assert False, ComplectItem.objects.filter(complect = self).order_by('order')[0].product.image1
        return ComplectItem.objects.filter(complect = self).order_by('order')


    @property
    def active(self):
        active = True
        for item in self.items:
            if item.price == 0:
                active = False
        return active


    @property
    def price(self):
        price = 0
        for one in self.items:
            price += float(one.price)

        return price


class ComplectItem(models.Model):
    product = models.ForeignKey(ColorProduct, blank=True, related_name='color_complectitem', verbose_name=u"Продукт")
    complect = models.ForeignKey(Complect, blank=True, related_name='color_complect', verbose_name=u"Фильтр")
    # price = models.IntegerField(verbose_name=u'Цена', default=0)
    percent = models.IntegerField(verbose_name=u'Процент', default=0)
    order = models.IntegerField(verbose_name=u'Порядок', default=0)

    @property
    def price(self):
        if self.percent:
            price = round(self.product.price * (100 - self.percent) / 100)
        else:
            price = self.product.price

        return price


    def __unicode__(self):
        return self.product.name + ' ' + str(self.price)

    class Meta:
        verbose_name_plural = "Один комплект"




class ExtraCategory(models.Model):
    product_from = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт")
    categort_to = models.ForeignKey(Category, blank=True, verbose_name=u"Категория")
    count = models.IntegerField(verbose_name="Количество товаров", default=0, blank=True, null=True)


class ProductViews(models.Model):
    product = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт")
    date = models.DateField(default=datetime.date.today, blank=True, verbose_name="Дата публикации")
    ip_address = models.GenericIPAddressField(verbose_name=u'IP Address')


class Order(models.Model):

    CHECKOUT = (
        (1, 'Наличными'),
        (2, 'Приват 24'),
    )

    DELIVERY = (
        (1, 'Самовывоз'),
        (2, 'Курьером'),
        (3, 'Новая почта'),
    )

    user = models.ForeignKey(User, blank=True, null=True, verbose_name=u'Юзер')
    name = models.CharField(verbose_name=u'Имя', max_length=250, blank=True)
    lastname = models.CharField(verbose_name=u'Фамилия', max_length=250, blank=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=250)
    email = models.EmailField(verbose_name=u'Email', blank=True, null=True)
    product = models.ManyToManyField(Product, through='OrderProduct', verbose_name=u'Продукты')
    color = models.ManyToManyField(ColorProduct, through='OrderColor', verbose_name=u'Цвета')
    countprice = models.IntegerField(verbose_name=u'Количество', default=0)
    allprice = models.IntegerField(verbose_name=u'Цена', default=0)
    payment = models.IntegerField(verbose_name=u'Способ оплаты', choices=CHECKOUT, default=1)
    delivery = models.IntegerField(verbose_name=u'Способы доставки', choices=DELIVERY, default=1)
    proccessed = models.BooleanField(verbose_name="Обработан", default=False)
    pub_date = models.DateTimeField( default=datetime.datetime.now, blank=True, verbose_name="Дата публикации")
    allproducts = models.TextField(verbose_name=u'Все продукты', default="")

    def updateproduct(self):
        products = OrderProduct.objects.filter(order=self)
        colors = OrderColor.objects.filter(order=self)
        complects = OrderComplect.objects.filter(order = self)

        allprice = 0
        allproducts = ''
        if products:
            for one in products:
                allprice += one.price*one.count
                if allproducts:
                    allproducts = allproducts + ', ' + one.product.name + ' ' + str(one.count) + 'x' + str(one.price)
                else:
                    allproducts = one.product.name  + ' ' + str(one.count) + 'x' + str(one.price)

        if colors:
            for one in colors:
                allprice += one.price*one.count
                if allproducts:
                    allproducts = allproducts + ', ' + one.color.product.name + ' ' + one.color.name  + ' ' + str(one.count) + 'x' + str(one.price)
                else:
                    allproducts = one.color.product.name + ' ' + one.color.name  + ' ' + str(one.count) + 'x' + str(one.price)

        if complects:
            for one in complects:
                allprice += one.price*one.count
                if allproducts:
                    allproducts = allproducts + ', ' + one.complect.name  + ' ' + str(one.count) + 'x' + str(one.price)
                else:
                    allproducts = one.complect.name  + ' ' + str(one.count) + 'x' + str(one.price)

        self.allproducts = allproducts
        self.allprice = allprice
        self.save()

    def products(self):
        products = OrderProduct.objects.filter(order=self)
        return products

    def colors(self):
        products = OrderColor.objects.filter(order=self)
        return products

    def complects(self):
        products = OrderComplect.objects.filter(order=self)
        return products




class OrderProduct(models.Model):
    """docstring for OrderProduct"""
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    product = models.ForeignKey(Product, verbose_name=u'Продукт')
    price = models.DecimalField(verbose_name=u'Цена', default=0, max_digits=7, decimal_places=2)
    count = models.IntegerField(verbose_name=u'Количество', default=0)

    @property
    def countprice(self):
        return self.price * self.count

    def save(self):
        super(OrderProduct,self).save()
        self.order.updateproduct()


class OrderComplect(models.Model):
    """docstring for OrderProduct"""
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    complect = models.ForeignKey(Complect, verbose_name=u'Комплект')
    price = models.DecimalField(verbose_name=u'Цена', default=0, max_digits=7, decimal_places=2)
    count = models.IntegerField(verbose_name=u'Количество', default=0)


    @property
    def countprice(self):
        return self.price * self.count

    def save(self):
        super(OrderComplect,self).save()
        self.order.updateproduct()

class OrderColor(models.Model):
    """docstring for OrderProduct"""
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    color = models.ForeignKey(ColorProduct, verbose_name=u'Цвет товара')
    price = models.DecimalField(verbose_name=u'Цена', default=0, max_digits=7, decimal_places=2)
    count = models.IntegerField(verbose_name=u'Количество', default=0)

    @property
    def countprice(self):
        return self.price * self.count

    def save(self):
        super(OrderColor,self).save()
        self.order.updateproduct()

class OrderPlace(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'Заказ', blank=True, null=True)
    place = models.CharField(verbose_name=u'Адресс доставки', max_length=255)


class OrderDelivery(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'Заказ', blank=True, null=True)
    deliveryservice = models.CharField(verbose_name=u'Служба доставки', max_length=255, default=0)



class Articles(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    image = ThumbnailImageField(upload_to=make_upload_path, blank=True,  verbose_name="Изображение")
    category = models.ForeignKey(Category, blank=True, verbose_name="Категория")
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    slug = models.CharField(max_length=250, blank=True, verbose_name="Урл")
    short_text = RedactorField(blank=True, verbose_name="Короткое описание")
    full_text = RedactorField(blank=True, verbose_name="Полное описание")
    pub_date = models.DateField( default=datetime.date.today, blank=True, verbose_name="Дата публикации")
    published = models.BooleanField(verbose_name="Опубликован", default=False)
    ordering = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True, null=True)

    def get_url(self):
        try:
            return '/usfull/%s/' % (self.slug)
        except:
            pass

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Статьи"

class QuikOrder(models.Model):
    phone = models.CharField(max_length=250, verbose_name="Телефон")
    producttext = models.CharField(max_length=250, verbose_name="Телефон")
    product = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт")
    proccessed = models.BooleanField(verbose_name="Обработан", default=False)
    pub_date = models.DateTimeField( default=datetime.datetime.now, blank=True, verbose_name="Дата публикации")

    def __unicode__(self):
        return self.phone
    class Meta:
        verbose_name_plural = "Быстрый заказ"


class NoOrder(models.Model):
    phone = models.CharField(max_length=250, verbose_name="Телефон")
    email = models.CharField(max_length=250, verbose_name="Email")
    name = models.CharField(max_length=250, verbose_name="Имя")
    producttext = models.CharField(max_length=250, verbose_name="Телефон")
    product = models.ForeignKey(Product, blank=True, verbose_name=u"Продукт")
    proccessed = models.BooleanField(verbose_name="Обработан", default=False)
    pub_date = models.DateTimeField( default=datetime.datetime.now, blank=True, verbose_name="Дата публикации")

    def __unicode__(self):
        return self.phone
    class Meta:
        verbose_name_plural = "Когда появится"


class Seo(models.Model):
    category = models.ForeignKey(Category, null=True,  verbose_name=u"Категория")
    fil = models.ForeignKey(FilterSelect, null=True,  verbose_name=u"Категория")
    name = models.CharField(verbose_name=u'Название', max_length=250)
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    full_text = RedactorField(blank=True, verbose_name="Короткое описание")
    def get_url(self):
        if self.fil:
            if not self.fil.slug:
                self.fil.slug = slugify(self.fil.value)
                self.fil.save()
        try:
            return '/catalog/%s/%s/' % (self.category.slug, self.fil.slug)
        except:
            pass

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Seo страницы"
        verbose_name = "Seo страница"


class SeoBrand(models.Model):
    category = models.ForeignKey(Category, null=True,  verbose_name=u"Категория")
    brand = models.ForeignKey(Brand, null=True,  verbose_name=u"Категория")
    name = models.CharField(verbose_name=u'Название', max_length=250)
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    full_text = RedactorField(blank=True, verbose_name="Короткое описание")

    def get_url(self):

        try:
            return '/%s/%s/' % (self.category.slug, self.brand.slug)
        except:
            pass

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Seo Бренды"
        verbose_name = "Seo бренды"


class LowPrice(models.Model):
    category = models.ForeignKey(Category, null=True,  verbose_name=u"Категория")
    name = models.CharField(verbose_name=u'Название', max_length=250)
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    full_text = RedactorField(blank=True, verbose_name="Короткое описание")
    def get_url(self):

        try:
            return '/nedorogo/%s/' % self.category.slug
        except:
            pass

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Seo Недорого"
        verbose_name = "Seo недорого"

class Popular(models.Model):
    category = models.ForeignKey(Category, null=True,  verbose_name=u"Категория")
    name = models.CharField(verbose_name=u'Название', max_length=250)
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Описание")
    full_text = RedactorField(blank=True, verbose_name="Короткое описание")
    def get_url(self):

        try:
            return '/poplyarnue/%s/' % self.category.slug
        except:
            pass

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Seo Популярные"
        verbose_name = "Seo популярные"

class BrandDescription(models.Model):
    category = models.ForeignKey(Category, null=True,  verbose_name=u"Категория")
    brand = models.ForeignKey(Brand, null=True,  verbose_name=u"Бренд")
    title = models.CharField(max_length=250, blank=True, verbose_name="Заголовок в браузере")
    metaKey = models.CharField(max_length=250, blank=True, verbose_name="Ключевые слова")
    metaDesc = models.CharField(max_length=250, blank=True, verbose_name="Мета описание")
    full_text = RedactorField(blank=True, verbose_name="Описание бренда")
    class Meta:
        verbose_name_plural = "Seo Описания для брендов"
        verbose_name = "Seo описание для бренда"


class Statistica(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=u'Юзер')
    session_id = models.CharField(verbose_name=u'Session', max_length=250, blank=True)
    color = models.ForeignKey(ColorProduct, verbose_name=u'Цвета')
    pub_date = models.DateTimeField( default=datetime.datetime.now, blank=True, verbose_name="Дата публикации")
    source = models.CharField(verbose_name=u'Source', max_length=250, blank=True)
    keywords = models.CharField(verbose_name=u'Keywords', max_length=250, blank=True)
    startpage = models.CharField(verbose_name=u'Startpage', max_length=250, blank=True)
    text = models.TextField(verbose_name=u'Где ходил', default="")

    class Meta:
        verbose_name_plural = "Статистики"
        verbose_name = "Статистика"

# url
# name
# is_index
# keywords
# type
# ext-id
# pubdate
class Ecomerce(MPTTModel):
    TYPES = (
        (1, "category"),
        (2, "category brand"),
        (3, "category filter"),
        (4, 'product'),
        (5, "product color"),
        (6, "folder"))

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u"Родительский пункт меню")
    url = models.CharField(verbose_name=u'Url', max_length=250, blank=True)
    name = models.CharField(verbose_name=u'Name', max_length=250, blank=True)
    keywords = models.TextField(verbose_name=u'Kewords', default="")
    is_index = models.BooleanField(verbose_name='В индексе', default=False)
    newnode = models.BooleanField(verbose_name='Новое', default=True)
    pub_date = models.DateTimeField( default=datetime.datetime.now, blank=True, verbose_name="Дата публикации")
    type = models.IntegerField(verbose_name=u'TYPE', default=0, choices=TYPES)
    source_id = models.IntegerField(verbose_name='Source id', default=0)

    def is_child(self):
        if Ecomerce.objects.filter(parent=self):
            return True
        else:
            return False

    def phrases(self):
        return EcomercePhrase.objects.filter(url=self, active=True)
         # items



    class Meta:
        verbose_name_plural = "Ecomerce"
        verbose_name = "Ecomerce"


class EcomercePhrase(models.Model):
    url = models.ForeignKey(Ecomerce, verbose_name='Url', blank=True, null=True)
    name = models.CharField(verbose_name=u'Name', max_length=250, blank=True)
    frequency_google = models.IntegerField(verbose_name=u'Frequency Adwords', default=0)
    frequency_yandex = models.IntegerField(verbose_name=u'Frequency Yandex', default=0)
    nowposition_google = models.IntegerField(verbose_name=u'Nowposition Google', default=0)
    nowposition_yandex = models.IntegerField(verbose_name=u'Nowposition Yandex', default=0)
    lastposition_google = models.IntegerField(verbose_name=u'Lastposition Google', default=0)
    lastposition_yandex = models.IntegerField(verbose_name=u'Lastposition Yandex', default=0)
    nofound = models.BooleanField(verbose_name='Не найдено', default=False)
    active = models.BooleanField(verbose_name='active', default=True)


class EcomercePosition(models.Model):
    url = models.ForeignKey(EcomercePhrase, verbose_name='phrase', blank=True, null=True)
    # name = models.CharField(verbose_name=u'Name', max_length=250, blank=True)
    position = models.IntegerField(verbose_name=u'position', default=0)
    pub_date = models.DateTimeField( default=datetime.datetime.now, blank=True, verbose_name="Дата публикации")


class EcomerceCaptcha(models.Model):
    request = models.IntegerField(verbose_name=u'Request', default=0)
    hiddenid = models.CharField(verbose_name=u'Hiddenid', max_length=250, blank=True, null=True)
    response = models.CharField(verbose_name=u'Response', max_length=250, blank=True, null=True)


class ProxyList(models.Model):
    list = models.TextField(verbose_name='List of proxy')

    def save(self):
        super(ProxyList,self).save()
        items = self.list.split('\n')
        for item in items:
            if not Proxy.objects.filter(name=item):
                Proxy(name=item).save()

    class Meta:
        verbose_name_plural = "ProxyList"
        verbose_name = "ProxyList"


class Proxy(models.Model):
    name = models.CharField(verbose_name=u'Name', max_length=250, blank=True)
    active = models.BooleanField(verbose_name='active', default=True)

    class Meta:
        verbose_name_plural = "Proxy"
        verbose_name = "Proxy"

    def __unicode__(self):
        return self.name


class Ancor(models.Model):
    ancor = models.CharField(max_length=250, verbose_name='Анкор')
    url = models.CharField(max_length=250, verbose_name='Урл')
    published = models.BooleanField(default=False, verbose_name='Опубликован')

    class Meta:
        verbose_name_plural = "Анкоры"
        verbose_name = "Анкоры"