# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_bars(apps, schema_editor):
    Bar = apps.get_model('inventory', 'Bar')
    Bar.objects.bulk_create([
        Bar(name="Women's Olympic", weight_kg='15'),
        Bar(name="Men's Olympic", weight_kg='20'),
    ])


def reverse_bars(apps, schema_editor):
    Bar = apps.get_model('inventory', 'Bar')
    Bar.objects.all().delete()


def make_lifts(apps, schema_editor):
    Lift = apps.get_model('inventory', 'Lift')
    Lift.objects.bulk_create([
        # bodybuilding.com links?
        Lift(name="Barbell Bench Press"),
        Lift(name="Barbell Curl"),
        Lift(name="Barbell Deadlift"),
        Lift(name="Barbell Squat"),
        Lift(name="Barbell Front Squat"),
        Lift(name="Barbell Deadlift"),
        Lift(name="Standing Overhead Press"),
        Lift(name="Barbell Row"),

        Lift(name="Pull Up"),
        Lift(name="Chin Up"),
        Lift(name="Push Up"),

        Lift(name="Dumbbell Curl"),
    ])

def reverse_lifts(apps, schema_editor):
    Lift = apps.get_model('inventory', 'Lift')
    Lift.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_bars, reverse_code=reverse_bars),
        migrations.RunPython(make_lifts, reverse_code=reverse_lifts),
    ]
