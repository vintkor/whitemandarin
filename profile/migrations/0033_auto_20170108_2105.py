# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-08 19:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0032_auto_20170108_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2017, 1, 8, 19, 5, 8, 587395, tzinfo=utc)),
        ),
    ]
