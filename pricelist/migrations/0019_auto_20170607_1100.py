# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-07 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0018_fileprovider_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileprovider',
            name='additionaldescription',
        ),
        migrations.RemoveField(
            model_name='fileprovider',
            name='additionalmodel',
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='description2',
            field=models.IntegerField(blank=True, default=0, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u043e\u043b\u043e\u043d\u043a\u0430 2'),
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='description3',
            field=models.IntegerField(blank=True, default=0, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u043e\u043b\u043e\u043d\u043a\u0430 3'),
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='model2',
            field=models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c \u043a\u043e\u043b\u043e\u043d\u043a\u0430 2'),
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='model3',
            field=models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c \u043a\u043e\u043b\u043e\u043d\u043a\u0430 3'),
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='price_rrc',
            field=models.IntegerField(blank=True, default=0, verbose_name='\u0426\u0435\u043d\u0430 \u043a\u043e\u043b\u043e\u043d\u043a\u0430 \u0420\u0420\u0426'),
        ),
        migrations.AddField(
            model_name='pricestring',
            name='price_grn_rrc',
            field=models.IntegerField(default=0, verbose_name='\u0426\u0435\u043d\u0430 \u0432 \u0433\u0440\u0438\u0432\u043d\u0430\u0445 \u0440\u0440\u0446'),
        ),
    ]