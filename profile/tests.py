from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class TestProfile(TestCase):

    def test_signal(self):

        u = User.objects.create_user(username='test', email='test@example.com', password='test')

        assert Profile.objects.filter(user=u).count() == 1
