# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-05 04:42
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('duration', models.DurationField()),
                ('frequency', models.PositiveSmallIntegerField(default=1)),
                ('days', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), default=list, size=None)),
                ('blocked_by', models.ManyToManyField(related_name='_chore_blocked_by_+', to='scheduler.Chore')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('chore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Chore')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scheduler.Person')),
            ],
        ),
    ]
