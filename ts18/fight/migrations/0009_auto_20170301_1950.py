# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fight', '0008_record_rpynumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='log',
            field=models.FilePathField(blank=True, null=True),
        ),
    ]
