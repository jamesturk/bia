from django.test import TestCase
from django.contrib.auth.models import User
from lifting.models import LiftingOptions


class TestLiftingOptions(TestCase):

    def test_signal(self):
        u = User.objects.create_user(username='test', email='test@example.com', password='test')
        assert LiftingOptions.objects.filter(user=u).count() == 1
