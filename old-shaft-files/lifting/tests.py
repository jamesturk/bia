from decimal import Decimal as D
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Exercise, UserSettings, ExerciseRules, Plan
from .plans import warmup_ss
from .utils import round_to


def _seteq(s1, exercise, weight, reps):
    try:
        assert s1.exercise == exercise
        assert s1.weight == weight
        assert s1.reps == reps
    except AssertionError:
        raise AssertionError('{0} != {1}x{2}'.format(s1, weight, reps))



class PlanTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user')
        self.squat = Exercise.objects.create(name='squat')
        self.bench = Exercise.objects.create(name='bench press')
        ExerciseRules.objects.create(user=self.user, exercise=self.squat, work_weight=200)
        ExerciseRules.objects.create(user=self.user, exercise=self.bench, work_weight=100)
        self.tm = Plan.objects.create(name='Texas Method')

        a1 = self.tm.days.create(name='A week - Volume day', order=1)
        a1.exercises.create(exercise=self.squat, order=1, sets='5,5,5,5,5', percent=D('0.85'))
        a1.exercises.create(exercise=self.bench, order=2, sets='5,5,5,5,5', percent=D('0.85'))

        a2 = self.tm.days.create(name='A week - Recovery day', order=2)
        a2.exercises.create(exercise=self.squat, order=1, sets='5,5', percent=D('0.8'))

        # exaggerated raise_weight for tests
        a3 = self.tm.days.create(name='A week - Record day', order=3)
        a3.exercises.create(exercise=self.squat, order=1, sets='5', percent=D(1),
                            raise_weight=True)
        a3.exercises.create(exercise=self.bench, order=2, sets='5', percent=D(1),
                            raise_weight=True)

        b1 = self.tm.days.create(name='B week - Volume day', order=4)
        b1.exercises.create(exercise=self.squat, order=1, sets='5,5,5,5,5', percent=D('0.85'))

        b2 = self.tm.days.create(name='B week - Recovery day', order=5)
        b2.exercises.create(exercise=self.squat, order=1, sets='5,5', percent=D('0.8'))
        b2.exercises.create(exercise=self.bench, order=1, sets='5,5', percent=D('0.8'))

        b3 = self.tm.days.create(name='B week - Record day', order=6)
        b3.exercises.create(exercise=self.squat, order=2, sets='5', percent=D(1))

    def test_get_days(self):
        a1, a2, a3, b1, b2, b3 = self.tm.get_days(self.user)

        _seteq(a1[0], self.squat, 170, 5)
        _seteq(a1[1], self.squat, 170, 5)
        _seteq(a1[2], self.squat, 170, 5)
        _seteq(a1[3], self.squat, 170, 5)
        _seteq(a1[4], self.squat, 170, 5)
        _seteq(a1[5], self.bench, 85, 5)
        _seteq(a1[6], self.bench, 85, 5)
        _seteq(a1[7], self.bench, 85, 5)
        _seteq(a1[8], self.bench, 85, 5)
        _seteq(a1[9], self.bench, 85, 5)

        _seteq(a2[0], self.squat, 160, 5)
        _seteq(a2[1], self.squat, 160, 5)

        _seteq(a3[0], self.squat, 200, 5)
        _seteq(a3[1], self.bench, 100, 5)

        # b record day raised by 5
        _seteq(b3[0], self.squat, 205, 5)


class WarmupTests(TestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(name='bench press')
        self.user = User.objects.create_user(username='user')

    def test_round_to(self):
        assert round_to(D('21'), D('2.5')) == D('20')
        assert round_to(D('23'), D('2.5')) == D('22.5')
        assert round_to(D('23'), D('5')) == D('20')
        assert round_to(D('24.5'), D('2.5')) == D('22.5')
        assert round_to(D('24.9'), D('5')) == D('25')

    def test_warmup_ss(self):
        # <=55: no warmup
        assert warmup_ss(self.exercise, D('10'), self.user) == []
        assert warmup_ss(self.exercise, D('55'), self.user) == []

        # 60: just the bar
        sets = warmup_ss(self.exercise, D('60'), self.user)
        assert len(sets) == 2, sets
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)

        sets = warmup_ss(self.exercise, D('70'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 55, 2)

        sets = warmup_ss(self.exercise, D('95'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 55, 3)
        _seteq(sets[3], self.exercise, 75, 2)

        sets = warmup_ss(self.exercise, D('135'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 50, 5)
        _seteq(sets[3], self.exercise, 80, 3)
        _seteq(sets[4], self.exercise, 105, 2)

        sets = warmup_ss(self.exercise, D('170'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 65, 5)
        _seteq(sets[3], self.exercise, 100, 3)
        _seteq(sets[4], self.exercise, 135, 2)

        sets = warmup_ss(self.exercise, D('250'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 100, 5)
        _seteq(sets[3], self.exercise, 150, 3)
        _seteq(sets[4], self.exercise, 200, 2)

        # slightly crazy jump
        sets = warmup_ss(self.exercise, D('315'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 125, 5)
        _seteq(sets[3], self.exercise, 185, 3)
        _seteq(sets[4], self.exercise, 250, 2)

        # this is probably crazy & should be fixed
        sets = warmup_ss(self.exercise, D('500'), self.user)
        _seteq(sets[0], self.exercise, 45, 5)
        _seteq(sets[1], self.exercise, 45, 5)
        _seteq(sets[2], self.exercise, 200, 5)
        _seteq(sets[3], self.exercise, 300, 3)
        _seteq(sets[4], self.exercise, 400, 2)
