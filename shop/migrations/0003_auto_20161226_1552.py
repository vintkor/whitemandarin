# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-26 13:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20161226_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 26, 15, 52, 33, 188182), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
