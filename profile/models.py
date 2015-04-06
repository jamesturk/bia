from django.db import models
from django.contrib.auth.models import User

UNITS = (
    ('m', 'Metric (kg)'),
    ('i', 'Imperial (lbs)'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    lifting_units = models.CharField(max_length=1, choices=UNITS)

    def metric(self):
        return self.lifting_units == 'm'
