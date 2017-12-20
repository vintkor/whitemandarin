# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-04 21:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20170102_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdelivery',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xbe\xd0\xba \xd1\x81\xd0\xbe\xd1\x80\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb8'),
        ),
        migrations.AddField(
            model_name='orderdelivery',
            name='text',
            field=models.TextField(default=b'', verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='orderpayment',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xbe\xd0\xba \xd1\x81\xd0\xbe\xd1\x80\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 4, 23, 50, 52, 357643), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='od', to='shop.OrderDelivery', verbose_name='\u0421\u043f\u043e\u0441\u043e\u0431\u044b \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op', to='shop.OrderPayment', verbose_name='\u0421\u043f\u043e\u0441\u043e\u0431 \u043e\u043f\u043b\u0430\u0442\u044b'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 4, 23, 50, 52, 362325), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='product',
            name='customdays',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbb\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe \xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9'),
        ),
        migrations.AlterField(
            model_name='product',
            name='idcode',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xb4 \xd1\x82\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80\xd0\xb0'),
        ),
    ]