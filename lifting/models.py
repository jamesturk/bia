from django.db import models

SET_TYPES = (
    ('warmup', 'Warmup'),
    ('planned', 'Planned'),
)


class Exercise(models.Model):
    name = models.CharField(max_length=200)


class Set(models.Model):
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, related_name='sets')
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)
    reps = models.PositiveIntegerField()
    source = models.CharField(max_length=100)
