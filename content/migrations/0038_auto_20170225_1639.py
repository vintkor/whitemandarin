# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-25 14:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0037_auto_20170217_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 2, 25, 14, 39, 18, 388557, tzinfo=utc), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
