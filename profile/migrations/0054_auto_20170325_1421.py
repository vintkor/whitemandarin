# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-25 12:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0053_auto_20170325_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2017, 3, 25, 12, 20, 56, 357589, tzinfo=utc)),
        ),
    ]
