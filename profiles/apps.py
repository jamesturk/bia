from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


def create_profile(sender, created, instance, **kwargs):
    from .models import Profile
    if created:
        Profile.objects.create(user=instance)


class ProfileConfig(AppConfig):
    name = 'profiles'
    app_label = 'profiles'

    def ready(self):
        post_save.connect(create_profile, sender=User)
