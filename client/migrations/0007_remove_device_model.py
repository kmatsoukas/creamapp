# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 10:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_trasfer_devices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='model',
        ),
    ]
