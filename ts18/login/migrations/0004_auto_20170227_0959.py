# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-27 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_member_scores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(default='head_images/customer.png', upload_to='head_images'),
        ),
    ]
