# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '3000_initial_data'),
        ('lifting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='liftingoptions',
            name='default_bar',
            field=models.ForeignKey(default=1, to='inventory.Bar'),
            preserve_default=False,
        ),
    ]
