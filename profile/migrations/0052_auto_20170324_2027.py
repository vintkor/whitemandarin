# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-24 18:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0051_auto_20170323_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2017, 3, 24, 18, 27, 51, 714154, tzinfo=utc)),
        ),
    ]
