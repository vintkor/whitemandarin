# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-18 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0003_auto_20170412_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='nal',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='nalrow',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='nalsym',
        ),
        migrations.AlterField(
            model_name='provider',
            name='path',
            field=models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u041f\u0443\u0442\u044c \u043a \u043f\u0430\u043f\u043a\u0435 \u0441 \u043f\u0440\u0430\u0439\u0441\u0430\u043c\u0438 \u0432 \u0434\u0440\u043e\u043f\u0431\u043e\u043a\u0441\u0435'),
        ),
    ]