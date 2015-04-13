from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from inventory.models import Lift, Bar

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
    default_bar = models.ForeignKey(Bar, default=1)
    plate_pairs = ArrayField(models.DecimalField(max_digits=7, decimal_places=3),
                             default=['45','45','25','10','5','5','2.5','1.25'])

    def plates_for_weight(self, weight):
        side = []
        w = Decimal(weight)
        if self.lifting_units == 'i':
            w -= self.default_bar.weight_lb
        else:
            w -= self.default_bar.weight_kg
        initial_weight = w
        available = sorted(self.plate_pairs, reverse=True)
        while w and available:
            plate = available.pop(0)
            if plate * 2 <= w:
                w -= plate * 2
                side.append(plate)
        if sum(side) * 2 != initial_weight:
            raise ValueError('remaining weight {}'.format(initial_weight - sum(side) * 2))
        return side

class Set(models.Model):
    user = models.ForeignKey(User, related_name='sets')
    date = models.DateField()
    lift = models.ForeignKey(Lift, related_name='sets')
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)
    reps = models.PositiveIntegerField()
    source = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {} @ {}kg - {}'.format(self.lift, self.reps, self.weight_kg, self.date)
