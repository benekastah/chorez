# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_auto_20170706_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='chore',
            name='last_done',
            field=models.DateField(blank=True, null=True),
        ),
    ]
