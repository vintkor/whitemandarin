# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 12:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20170109_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('order', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xbe\xd0\xba \xd1\x81\xd0\xbe\xd1\x80\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb8')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u0438\u0441\u043a\u043e\u0432\u044b\u0435 \u0437\u0430\u043f\u0440\u043e\u0441\u044b',
                'verbose_name_plural': '\u041f\u043e\u0438\u0441\u043a\u043e\u0432\u044b\u0435 \u0437\u0430\u043f\u0440\u043e\u0441\u044b ',
            },
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 9, 14, 7, 36, 312178), null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 9, 14, 7, 36, 316449), null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
    ]
