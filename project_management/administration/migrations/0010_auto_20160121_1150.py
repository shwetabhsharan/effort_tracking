# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0009_auto_20160121_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codereview',
            name='status',
            field=models.CharField(choices=[('Opem', 'Open'), ('In Progress', 'In Progress'), ('Fixed', 'Fixed'), ('Closed', 'Closed'), ('No Comments', 'No Comments')], max_length=30),
        ),
    ]
