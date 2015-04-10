# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiftingOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('lifting_units', models.CharField(default='i', choices=[('m', 'Metric (kg)'), ('i', 'Imperial (lb)')], max_length=1)),
                ('plate_pairs', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(max_digits=7, decimal_places=3), default=['45', '45', '25', '10', '5', '5', '2.5', '1.25'], size=None)),
                ('user', models.OneToOneField(related_name='lifting_options', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('weight_kg', models.DecimalField(max_digits=7, decimal_places=3)),
                ('reps', models.PositiveIntegerField()),
                ('source', models.CharField(max_length=100)),
                ('lift', models.ForeignKey(related_name='sets', to='inventory.Lift')),
                ('user', models.ForeignKey(related_name='sets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
