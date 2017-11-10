# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 05:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0021_remove_comment_my_posts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_item', to='post.Post')),
                ('post_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_item', to='post.Post')),
            ],
        ),
    ]
