# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-02 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0006_pricestring_garantee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricestring',
            name='price',
            field=models.IntegerField(default=0, verbose_name='\u0426\u0435\u043d\u0430 \u0432 \u0432\u0430\u043b\u044e\u0442\u0435 \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430'),
        ),
        migrations.AlterField(
            model_name='pricestring',
            name='price_grn',
            field=models.IntegerField(default=0, verbose_name='\u0426\u0435\u043d\u0430 \u0432 \u0433\u0440\u0438\u0432\u043d\u0430\u0445'),
        ),
    ]