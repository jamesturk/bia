# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifting', '0002_liftingoptions_default_bar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liftingoptions',
            name='default_bar',
            field=models.ForeignKey(default=1, to='inventory.Bar'),
        ),
    ]
