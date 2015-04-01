from django.db import models
from django.contrib.postgres.fields import ArrayField

SET_TYPES = (
    ('warmup', 'Warmup'),
    ('planned', 'Planned'),
)


class Exercise(models.Model):
    names = ArrayField(models.CharField(max_length=200))

    def __str__(self):
        return self.names


class Set(models.Model):
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, related_name='sets')
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)
    reps = models.PositiveIntegerField()
    source = models.CharField(max_length=100)
