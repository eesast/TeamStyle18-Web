# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0018_auto_20170301_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfile',
            name='permissions',
            field=models.CharField(choices=[('2', '登陆可见'), ('1', '公开')], max_length=1),
        ),
    ]
