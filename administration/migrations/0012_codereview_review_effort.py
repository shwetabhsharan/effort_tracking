# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0011_auto_20160125_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='codereview',
            name='review_effort',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=False,
        ),
    ]
