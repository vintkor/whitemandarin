# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-07 10:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0052_auto_20170406_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=250, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd')),
                ('email', models.CharField(max_length=250, verbose_name=b'Email')),
                ('name', models.CharField(max_length=250, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('proccessed', models.BooleanField(default=False, verbose_name=b'\xd0\x9e\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xb0\xd0\xbd')),
                ('pub_date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='\u041f\u0440\u043e\u0434\u0443\u043a\u0442')),
            ],
            options={
                'verbose_name_plural': '\u041a\u043e\u0433\u0434\u0430 \u043f\u043e\u044f\u0432\u0438\u0442\u0441\u044f',
            },
        ),
    ]