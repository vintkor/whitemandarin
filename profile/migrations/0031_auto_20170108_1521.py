# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-08 13:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0030_auto_20170108_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2017, 1, 8, 13, 21, 23, 347117, tzinfo=utc)),
        ),
    ]