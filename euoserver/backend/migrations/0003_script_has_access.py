# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_script_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='has_access',
            field=models.BooleanField(default=True, verbose_name='require access'),
        ),
    ]