# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-27 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fight', '0004_auto_20170225_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='AI1_scorechange',
        ),
        migrations.RemoveField(
            model_name='record',
            name='AI2_scorechange',
        ),
        migrations.RemoveField(
            model_name='record',
            name='result',
        ),
        migrations.AddField(
            model_name='record',
            name='scorechange',
            field=models.IntegerField(default=0),
        ),
    ]
