# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-08 19:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_auto_20170108_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 8, 21, 20, 18, 180219), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 8, 21, 20, 18, 186108), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
