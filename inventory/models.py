from django.db import models
from common import remove_exponent, to_lb


class Bar(models.Model):
    name = models.CharField(max_length=100)
    weight_kg = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return '{} ({}kg / {}lb)'.format(self.name, remove_exponent(self.weight_kg),
                                         self.weight_lb)

    @property
    def weight_lb(self):
        return to_lb(self.weight_kg)


class Lift(models.Model):
    name = models.CharField(max_length=200)

    @property
    def display_name(self):
        return self.name

    def __str__(self):
        return self.name

