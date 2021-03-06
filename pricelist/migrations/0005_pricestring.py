# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 09:33
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0004_auto_20170418_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(blank=True, max_length=250, verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430')),
                ('brand', models.CharField(blank=True, max_length=250, verbose_name='\u0411\u0440\u0435\u043d\u0434')),
                ('articul', models.CharField(blank=True, max_length=250, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b')),
                ('model', models.TextField(blank=True, null=True, verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c')),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('searchindex', models.TextField(blank=True, null=True, verbose_name='\u041f\u043e\u0438\u0441\u043a\u043e\u0432\u044b\u0439 \u0438\u043d\u0434\u0435\u043a\u0441')),
                ('linked', models.BooleanField(default=False, verbose_name=b'Linked')),
                ('changed', models.BooleanField(default=True, verbose_name=b'\xd0\x98\xd0\xb7\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xbe')),
                ('inproducts', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name=b'Products')),
                ('inhotline', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name=b'Hotline')),
                ('inprice', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name=b'Price')),
                ('price', models.IntegerField(default=0, verbose_name='Price min')),
                ('price_grn', models.IntegerField(default=0, verbose_name='Price min')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricelist.Provider', verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd1\x89\xd0\xb8\xd0\xba')),
            ],
            options={
                'verbose_name': '!\u0421\u0442\u0440\u043e\u0447\u043a\u0430 \u043f\u0440\u0430\u0439\u0441\u043e\u0432',
                'verbose_name_plural': '!\u0421\u0442\u0440\u043e\u0447\u043a\u0430 \u043f\u0440\u0430\u0439\u0441\u0430',
            },
        ),
    ]
