# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0005_pricestring'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricestring',
            name='garantee',
            field=models.IntegerField(default=0, verbose_name='\u0413\u0430\u0440\u0430\u043d\u0442\u0438\u044f'),
        ),
    ]