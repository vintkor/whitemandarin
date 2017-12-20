# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-02 10:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20161228_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=250, verbose_name=b'Ip')),
                ('name', models.CharField(max_length=250, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('email', models.CharField(max_length=250, verbose_name=b'email')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x80\xd1\x82')),
            ],
            options={
                'verbose_name': 'Subsctibe',
                'verbose_name_plural': 'Subscribe',
            },
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 2, 12, 2, 28, 31104), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='product',
            name='oldprice',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x80\xd0\xb0\xd1\x8f \xd1\x86\xd0\xb5\xd0\xbd\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name=b'\xd0\xa6\xd0\xb5\xd0\xbd\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='product',
            name='reit',
            field=models.DecimalField(blank=True, decimal_places=1, default=5.0, max_digits=2, null=True, verbose_name=b'\xd0\xa0\xd0\xb5\xd0\xb9\xd1\x82\xd0\xb8\xd0\xbd\xd0\xb3'),
        ),
    ]