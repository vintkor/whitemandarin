# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-06 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0016_auto_20170606_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='currency',
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='excellist',
            field=models.IntegerField(blank=True, default=0, verbose_name='\u041b\u0438\u0441\u0442 \u044d\u043a\u0441\u0435\u043b\u044f, \u0435\u0441\u043b\u0438 0 \u0437\u043d\u0430\u0447\u0438\u0442 \u0432\u0441\u0435 \u0438\u043b\u0438 \u0442\u043e\u043b\u044c\u043a\u043e'),
        ),
    ]
