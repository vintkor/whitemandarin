# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-08 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0053_noorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcurentHotline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0, verbose_name=b'position')),
                ('price', models.IntegerField(default=0, verbose_name=b'price')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
        migrations.CreateModel(
            name='FirmHotline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('url', models.CharField(max_length=250, verbose_name=b'Url')),
                ('itemid', models.IntegerField(default=0, verbose_name=b'itemid')),
                ('pub_date', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8')),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0438\u0440\u043c\u044b',
                'verbose_name_plural': '\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0438\u0440\u043c',
            },
        ),
        migrations.CreateModel(
            name='OneHotline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0, verbose_name=b'Position')),
                ('total', models.IntegerField(default=0, verbose_name=b'Total')),
                ('max', models.IntegerField(default=0, verbose_name=b'Max')),
                ('min', models.IntegerField(default=0, verbose_name=b'Min')),
                ('concurents', models.TextField(default=b'', verbose_name=b'Concurents')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ColorProduct', verbose_name=b'Product')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
        migrations.CreateModel(
            name='ScanHotline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8')),
                ('items', models.IntegerField(default=0, verbose_name=b'items')),
                ('nowitems', models.IntegerField(default=0, verbose_name=b'items')),
                ('started', models.BooleanField(default=False, verbose_name=b'\xd0\x9d\xd0\xb0\xd1\x87\xd0\xb0\xd0\xbb\xd1\x81\xd1\x8f')),
                ('finished', models.BooleanField(default=False, verbose_name=b'\xd0\x97\xd0\xb0\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd0\xb5\xd0\xbd')),
                ('lastitems', models.IntegerField(default=0, verbose_name=b'lastitems')),
                ('pause', models.IntegerField(default=0, verbose_name=b'Pause')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category', verbose_name=b'Category')),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0438\u0440\u043c\u044b',
                'verbose_name_plural': '\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0438\u0440\u043c',
            },
        ),
        migrations.AddField(
            model_name='onehotline',
            name='scan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotline.ScanHotline', verbose_name=b'ScanHotline'),
        ),
        migrations.AddField(
            model_name='concurenthotline',
            name='firm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotline.FirmHotline', verbose_name=b'FirmHotline'),
        ),
        migrations.AddField(
            model_name='concurenthotline',
            name='one',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotline.OneHotline', verbose_name=b'OneHotline'),
        ),
    ]
