# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-05 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0014_provider_dropbox_dir'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileprovider',
            name='dropbox_file',
            field=models.CharField(blank=True, choices=[(b'-', b'-')], default=b'', max_length=250, verbose_name='Dropbox File'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='dropbox_dir',
            field=models.CharField(blank=True, choices=[(b'-', b'-')], default=b'', max_length=250, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
