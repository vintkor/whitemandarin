# -*- coding: utf-8 -*-
import os
from django.db import models


class Reit(models.Model):
    vote = models.DecimalField(max_digits=2, decimal_places=1,db_index=True, verbose_name="Оценка")
    date_add = models.DateTimeField(auto_now_add=True, verbose_name="Оценка")
    item_id = models.IntegerField(null=True, blank=True, verbose_name="Товар" )
    paket = models.CharField(max_length=200, db_index=True,blank=True, verbose_name="Название")
    model_name = models.CharField(max_length=200, db_index=True,blank=True, verbose_name="Название")
    def __unicode__(self):
        return self.vote
    class Meta:
        verbose_name_plural = "Разделы"
        verbose_name = "Раздел"
