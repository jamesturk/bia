from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from common import to_lb

UNITS = (
    ('m', 'Metric (kg)'),
    ('i', 'Imperial (lb)'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    lifting_units = models.CharField(max_length=1, choices=UNITS, default='i')
    plate_pairs = ArrayField(models.DecimalField(max_digits=7, decimal_places=3),
                             default=['45','45','25','10','5','5','2.5','1.25'])


class Bar(models.Model):
    user = models.OneToOneField(User, related_name='bar')

    name = models.CharField(max_length=100)
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return '{} ({}lb / {}kg)'.format(self.name, self.weight_kg, self.weight_lb)

    @property
    def weight_lb(self):
        return to_lb(self.weight_kg)
