from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

SET_TYPES = (
    ('warmup', 'Warmup'),
    ('planned', 'Planned'),
)


class Exercise(models.Model):
    names = ArrayField(models.CharField(max_length=200))

    def display_name(self):
        return self.names[0].title()

    def __str__(self):
        return ', '.join(self.names)


class Set(models.Model):
    user = models.ForeignKey(User, related_name='sets')
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, related_name='sets')
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)
    reps = models.PositiveIntegerField()
    source = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {} @ {}kg - {}'.format(self.exercise, self.reps, self.weight_kg, self.date)
