# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 17:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0015_auto_20161227_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2016, 12, 27, 17, 38, 28, 309640, tzinfo=utc)),
        ),
    ]
