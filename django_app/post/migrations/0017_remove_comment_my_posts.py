# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 05:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_auto_20170821_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='my_posts',
        ),
    ]
