# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-30 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0008_auto_20170530_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileprovider',
            name='availabilityequal',
            field=models.IntegerField(blank=True, choices=[(0, b'='), (1, b'<>'), (2, b'IN')], default=0, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c \u0442\u0438\u043f'),
        ),
    ]
