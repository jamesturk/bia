from decimal import Decimal as D
from django.test import TestCase
from django.contrib.auth.models import User
from lifting.models import LiftingOptions


class TestLiftingOptions(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@example.com', password='test')

    def test_signal(self):
        assert LiftingOptions.objects.filter(user=self.user).count() == 1

    def test_plates_for_weight(self):
        opts = self.user.lifting_options
        opts.plate_pairs = [D(45), D(45), D(25), D(10), D(5), D(5), D('2.5')]
        opts.default_bar_id = 1

        assert opts.plates_for_weight(45) == []
        assert opts.plates_for_weight(50) == [D('2.5')]
        assert opts.plates_for_weight(90) == [D(10), D(5), D(5), D('2.5')]
        assert opts.plates_for_weight(320) == [D(45), D(45), D(25), D(10), D(5), D(5), D('2.5')]

    def test_plates_for_weight_error(self):
        opts = self.user.lifting_options
        opts.plate_pairs = [D(45), D(45), D(25), D(10), D(5), D(5), D('2.5')]
        opts.default_bar_id = 1
        # TODO: check amounts
        with self.assertRaises(ValueError):
            opts.plates_for_weight('47.5')
        with self.assertRaises(ValueError):
            opts.plates_for_weight(325)
        with self.assertRaises(ValueError):
            opts.plates_for_weight(30)
