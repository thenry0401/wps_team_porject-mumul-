# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20170727_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('e', '전자제품'), ('f', '가구'), ('be', '뷰티'), ('c', '옷'), ('bo', '책'), ('o', '기타')], max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='trading_type',
            field=models.CharField(choices=[('d', '직거래'), ('p', '택배거래')], max_length=30),
        ),
    ]
