# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-21 12:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2016, 12, 21, 12, 20, 6, 445429, tzinfo=utc)),
        ),
    ]
