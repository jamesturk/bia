# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('weight_kg', models.DecimalField(max_digits=7, decimal_places=3)),
                ('user', models.OneToOneField(related_name='bar', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='plate_pairs',
            field=django.contrib.postgres.fields.ArrayField(default=['45', '45', '25', '10', '5', '5', '2.5', '1.25'], base_field=models.DecimalField(max_digits=7, decimal_places=3), size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lifting_units',
            field=models.CharField(default='i', choices=[('m', 'Metric (kg)'), ('i', 'Imperial (lb)')], max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
