# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-30 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pricelist', '0007_auto_20170502_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.IntegerField(blank=True, default=0, verbose_name='\u0411\u0440\u0435\u043d\u0434 \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('model', models.IntegerField(blank=True, default=0, verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('additionalmodel', models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043f\u043e\u043b\u044f \u043a \u043c\u043e\u0434\u0435\u043b\u0438')),
                ('articul', models.IntegerField(blank=True, default=0, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('description', models.IntegerField(blank=True, default=0, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('additionaldescription', models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043f\u043e\u043b\u044f \u043a \u043e\u043f\u0438\u0441\u043f\u043d\u0430\u043d\u0438\u044e')),
                ('garantee', models.IntegerField(blank=True, default=0, verbose_name='\u0413\u0430\u0440\u0430\u043d\u0442\u0438\u044f \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('garanteemonth', models.IntegerField(blank=True, default=0, verbose_name='\u0413\u0430\u0440\u0430\u043d\u0442\u0438\u044f \u043c\u0435\u0441\u044f\u0446\u0435\u0432 \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('discount', models.IntegerField(blank=True, default=0, verbose_name='\u0421\u043a\u0438\u0434\u043a\u0430 \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('price', models.IntegerField(blank=True, default=0, verbose_name='\u0426\u0435\u043d\u0430 \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('availabilityrow', models.IntegerField(blank=True, default=0, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c \u043a\u043e\u043b\u043e\u043d\u043a\u0430')),
                ('availabilityequal', models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c \u0442\u0438\u043f')),
                ('availabilityvalue', models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
                ('availabilityuse', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x8f\xd1\x82\xd1\x8c \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c')),
                ('path', models.CharField(blank=True, default=b'', max_length=250, verbose_name='\u041f\u0443\u0442\u044c \u043a \u0444\u0430\u0439\u043b\u0443 \u0432 \u0434\u0440\u043e\u043f\u0431\u043e\u043a\u0441\u0435')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='provider',
            name='articul',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='description',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='garantee',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='garanteemonth',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='model',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='price',
        ),
        migrations.AddField(
            model_name='fileprovider',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricelist.Provider', verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd1\x89\xd0\xb8\xd0\xba'),
        ),
    ]
