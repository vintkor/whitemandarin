# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-06 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0017_auto_20170606_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileprovider',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricelist.Currency', verbose_name=b'\xd0\x92\xd0\xb0\xd0\xbb\xd1\x8e\xd1\x82\xd0\xb0'),
        ),
    ]
