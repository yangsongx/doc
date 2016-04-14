# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uc', '0002_auto_20160413_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountprofile',
            name='customization',
        ),
        migrations.AddField(
            model_name='corpusdata',
            name='rob',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='uc.RobotType'),
        ),
        migrations.AlterField(
            model_name='corpusdata',
            name='answer',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
