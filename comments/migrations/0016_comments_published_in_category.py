# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-20 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0015_auto_20170405_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='published_in_category',
            field=models.BooleanField(default=False),
        ),
    ]