# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 12:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0038_auto_20170109_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2017, 1, 9, 12, 7, 36, 301141, tzinfo=utc)),
        ),
    ]
