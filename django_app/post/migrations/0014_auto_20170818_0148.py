# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20170817_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='for_sale_created_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]