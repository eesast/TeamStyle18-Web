# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20170228_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(default='head_images/customer.png', upload_to='head_images'),
        ),
    ]
