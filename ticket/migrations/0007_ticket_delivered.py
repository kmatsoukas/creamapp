# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_auto_20161019_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
