# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tinymce import models as tinymce_model
import datetime

class Comments(MPTTModel):
    prod_name = models.CharField(max_length=250, blank=True, db_index=True, verbose_name="Название")
    paket = models.CharField(max_length=250, db_index=True, verbose_name="Пакет")
    item_model = models.CharField(max_length=250, db_index=True, verbose_name="Модель")
    item_id = models.IntegerField(db_index=True, null=True,  verbose_name="id")
    published_in_category = models.BooleanField(default=False, verbose_name='Показывать в категории')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u"Родитель")
    name = models.CharField(max_length=250, verbose_name="Название")
    text = tinymce_model.HTMLField(blank=True, verbose_name="Полное описание")
    published = models.BooleanField(verbose_name="Опубликован")
    date_add = models.DateTimeField(default=datetime.datetime.today ,verbose_name="Дата публикации")
    vote = models.DecimalField(max_digits=2, decimal_places=1,db_index=True, null=True, verbose_name="Оценка")
    positive = models.IntegerField(null=True, blank=True, default=0, verbose_name="Позитивных")
    negative = models.IntegerField(null=True, blank=True, default=0, verbose_name="Негативных")
    def save(self):
        super(Comments, self).save()
        try:
            paket = self.paket
            item_model = self.item_model
            id = self.item_id
            count_comments = Comments.objects.filter(paket=paket, item_model=item_model, item_id=int(id), published = True).count()
            # assert False, count_comments
            exec "from %s.models import %s" % (paket, item_model)
            p = eval("%s.objects.get(pk=%d)" % (item_model, int(id)))
            p.comments_count = count_comments
            min_vote = 5
            max_vote = 0
            all_reit = 0.0
            prod_votes = Comments.objects.filter(paket=paket, item_model=item_model, item_id=int(id), published = True).values('vote')
            for item in prod_votes:
                if min_vote > item['vote']:
                    min_vote = item['vote']
                if max_vote < item['vote']:
                    max_vote = item['vote']
                all_reit = all_reit + float(item['vote'])
            # assert False, min_vote
            p.min_reit = min_vote
            p.max_reit = max_vote
            p.reit = all_reit / count_comments
            p.save()
            self.prod_name = p.name
        except:
            pass
        super(Comments, self).save()
        if not self.date_add:
            self.date_add = datetime.datetime.today()
            super(Comments, self).save()

    def get_name(self):
        paket = self.paket
        item_model = self.item_model
        id = self.item_id
        # count_comments = Comments.objects.filter(paket=paket, item_model=item_model, item_id=int(id), published = True).count()
        # assert False, count_comments
        exec "from %s.models import %s" % (paket, item_model)
        p = eval("%s.objects.get(pk=%d)" % (item_model, int(id)))
        return p.name

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Коментарии "
        verbose_name = "Коментарий"
        ordering = ['-id']

    class MPTTMeta:
        order_insertion_by = ['name']


class Utility(models.Model):
    comment = models.ForeignKey(Comments, blank=True, null=True, verbose_name="Коммент")
    positive = models.BooleanField(verbose_name="Позитивная оценка")


    def __unicode__(self):
        return self.comment.name
    class Meta:
        verbose_name_plural = "Оценки"
        verbose_name = "Оценка"


