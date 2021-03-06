# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-29 08:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0056_auto_20170429_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorproduct',
            name='marga',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=11, null=True, verbose_name=b'\xd0\x9c\xd0\xb0\xd1\x80\xd0\xb6\xd0\xb0'),
        ),
        migrations.AddField(
            model_name='colorproduct',
            name='margapercent',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=11, null=True, verbose_name=b'\xd0\x9c\xd0\xb0\xd1\x80\xd0\xb6\xd0\xb0 \xd0\xb2 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x86\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0\xd1\x85'),
        ),
        migrations.AlterField(
            model_name='colorproduct',
            name='lastscan_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 29, 11, 29, 54, 649835), verbose_name=b'Lastsscan Date'),
        ),
    ]
