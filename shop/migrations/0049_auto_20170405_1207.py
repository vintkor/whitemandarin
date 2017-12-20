# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 09:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_auto_20170404_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='main',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8\xd1\x82\xd1\x8c'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 5), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 5), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='ecomerce',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 5, 12, 6, 59, 560836), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='ecomerceposition',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 5, 12, 6, 59, 563082), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 5, 12, 6, 59, 545239), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='product',
            name='action_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 5, 12, 6, 59, 521644), null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xb0\xd0\xbd\xd1\x87\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb0\xd0\xba\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 5), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='productviews',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 5), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='quikorder',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 5, 12, 6, 59, 554124), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='statistica',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 5, 12, 6, 59, 559714), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]