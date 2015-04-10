from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


def create_profile(sender, created, instance, **kwargs):
    from .models import LiftingOptions
    if created:
        LiftingOptions.objects.create(user=instance)


class LiftingConfig(AppConfig):
    name = 'lifting'
    app_label = 'lifting'

    def ready(self):
        post_save.connect(create_profile, sender=User)
