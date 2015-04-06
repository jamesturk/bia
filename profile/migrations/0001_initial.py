# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('lifting_units', models.CharField(max_length=1, choices=[('m', 'Metric (kg)'), ('i', 'Imperial (lbs)')])),
                ('user', models.OneToOneField(related_name='config', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
