# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 13:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0019_task_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='keywords',
        ),
    ]
