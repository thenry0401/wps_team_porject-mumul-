# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 05:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0018_comment_my_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='my_posts',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_posts', to='post.Post'),
        ),
    ]
