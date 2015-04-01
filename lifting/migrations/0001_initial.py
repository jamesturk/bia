# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('weight_kg', models.DecimalField(decimal_places=3, max_digits=7)),
                ('reps', models.PositiveIntegerField()),
                ('source', models.CharField(max_length=100)),
                ('exercise', models.ForeignKey(to='lifting.Exercise', related_name='sets')),
            ],
        ),
    ]
