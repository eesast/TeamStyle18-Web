# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-22 13:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20170221_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='summary',
        ),
    ]