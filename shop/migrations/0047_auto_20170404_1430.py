# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-04 11:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0046_auto_20170327_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 4), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 4), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='ecomerce',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 4, 14, 30, 15, 705606), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='ecomerceposition',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 4, 14, 30, 15, 707811), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 4, 14, 30, 15, 692849), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='product',
            name='action_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 4, 14, 30, 15, 674203), null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xb0\xd0\xbd\xd1\x87\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb0\xd0\xba\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pub_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 4), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='productviews',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2017, 4, 4), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='quikorder',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 4, 14, 30, 15, 699112), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='statistica',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 4, 4, 14, 30, 15, 704588), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
