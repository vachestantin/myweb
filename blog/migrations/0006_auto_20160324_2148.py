# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 12:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at', '-pk')},
        ),
    ]
