# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-26 08:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_auto_20161221_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2016, 12, 26, 8, 10, 2, 14816, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name=b'email address'),
        ),
    ]
