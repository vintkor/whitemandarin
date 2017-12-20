# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 17:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20161227_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='top',
            field=models.BooleanField(default=False, verbose_name=b'Top'),
        ),
        migrations.AddField(
            model_name='filteritem',
            name='image',
            field=models.ImageField(blank=True, upload_to=shop.models.make_upload_path, verbose_name=b'\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 27, 19, 32, 47, 298113), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
