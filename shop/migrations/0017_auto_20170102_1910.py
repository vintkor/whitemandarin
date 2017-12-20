# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-02 17:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20170102_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='metakey',
        ),
        migrations.RemoveField(
            model_name='category',
            name='metakey',
        ),
        migrations.RemoveField(
            model_name='product',
            name='metakey',
        ),
        migrations.AddField(
            model_name='product',
            name='custom',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd0\xb7'),
        ),
        migrations.AddField(
            model_name='product',
            name='customdays',
            field=models.IntegerField(default=0, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbb\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe \xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9'),
        ),
        migrations.AddField(
            model_name='product',
            name='idcode',
            field=models.CharField(default='', max_length=250, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xb4 \xd1\x82\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80\xd0\xb0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 2, 19, 10, 0, 546873), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 2, 19, 10, 0, 550165), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]