# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0006_auto_20160120_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='team',
            field=models.CharField(choices=[('WETL', 'WETL'), ('Matrix', 'Matrix'), ('Gambit', 'Gambit'), ('Goonies', 'Goonies')], max_length=20, null=True),
        ),
    ]