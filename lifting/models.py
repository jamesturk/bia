from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from inventory.models import Lift

SET_TYPES = (
    ('warmup', 'Warmup'),
    ('planned', 'Planned'),
)

UNITS = (
    ('m', 'Metric (kg)'),
    ('i', 'Imperial (lb)'),
)


class LiftingOptions(models.Model):
    user = models.OneToOneField(User, related_name='lifting_options')

    lifting_units = models.CharField(max_length=1, choices=UNITS, default='i')
    plate_pairs = ArrayField(models.DecimalField(max_digits=7, decimal_places=3),
                             default=['45','45','25','10','5','5','2.5','1.25'])


class Set(models.Model):
    user = models.ForeignKey(User, related_name='sets')
    date = models.DateField()
    lift = models.ForeignKey(Lift, related_name='sets')
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)
    reps = models.PositiveIntegerField()
    source = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {} @ {}kg - {}'.format(self.lift, self.reps, self.weight_kg, self.date)
