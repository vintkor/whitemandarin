# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 11:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20170108_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='top',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\x9d\xd0\xb0 \xd0\xb3\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd0\xbe\xd0\xb9'),
        ),
        migrations.AddField(
            model_name='product',
            name='topimage',
            field=models.ImageField(blank=True, upload_to=shop.models.make_upload_path, verbose_name=b'\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbd\xd0\xb0 \xd0\xb3\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd0\xbe\xd0\xb9'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 9, 13, 32, 18, 574474), null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 9, 13, 32, 18, 578485), null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
