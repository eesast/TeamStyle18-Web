# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_auto_20170301_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfile',
            name='permissions',
            field=models.CharField(choices=[('1', '公开'), ('2', '登陆可见')], max_length=1),
        ),
    ]