# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 06:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0020_auto_20170821_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='my_posts',
        ),
    ]
