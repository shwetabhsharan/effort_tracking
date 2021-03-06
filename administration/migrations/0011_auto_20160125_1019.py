# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0010_auto_20160121_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codereview',
            name='fix_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='codereview',
            name='rca',
            field=models.CharField(choices=[('DOMO Standard', 'DOMO Standard'), ('AngularJS Experience', 'AngularJS Experience'), ('Client Code', 'Client Code'), ('Enhancement', 'Enhancement'), ('Code Optimization', 'Code Optimization'), ('Requirement Conflict', 'Requirement Conflict'), ('Reviewer Conflict', 'Reviewer Conflict'), ('Appreciation', 'Appreciation'), ('NA', 'NA')], max_length=30),
        ),
    ]
