# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20170802_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='post.Tag'),
        ),
    ]