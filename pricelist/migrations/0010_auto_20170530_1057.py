# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-30 07:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0009_auto_20170530_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='sizefile',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='upload',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='uploadtime',
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='sizefile',
            field=models.IntegerField(blank=True, default=0, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u0444\u0430\u0439\u043b\u0430'),
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to=b'uploads/', verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xb9\xd0\xbb'),
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='uploadtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9 \xd0\xb7\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb8'),
        ),
    ]