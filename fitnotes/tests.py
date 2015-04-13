from django.test import TestCase
from django.contrib.auth.models import User
from inventory.models import Lift
from lifting.models import Set
from .importer import import_fitnotes_db


class TestFitnotesImport(TestCase):
    # fitnotes.db has:
    # April 1
    #   bench press 10 @ 45
    #   bench press 5 @ 95
    #   bench press 3 @ 135
    #   bench press 5 @ 155
    # April 3
    #   squat 10 @ 45
    #   squat 5 @ 95
    #   squat 3 @ 135
    #   squat 2 @ 185
    #   squat 5 @ 225

    def setUp(self):
        self.user = User.objects.create_user('default', 'default@example.com', 'default')
        self.bench = Lift.objects.create(name='bench press')
        self.squat = Lift.objects.create(name='squat')

        self.good_mapping = {'flat barbell bench press': 'bench press',
                             'barbell squat': 'squat'
                            }
        self.bad_mapping = {'flat barbell bench press': 'bench press' }

    def test_basic_import(self):
        # ensure that the data comes in
        num = import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.good_mapping)
        assert num == 9
        assert Set.objects.filter(lift=self.bench).count() == 4
        assert Set.objects.filter(lift=self.squat).count() == 5

    def test_double_import(self):
        # two identical dbs, should be idempotent
        import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.good_mapping)
        import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.good_mapping)
        assert Set.objects.filter(lift=self.bench).count() == 4
        assert Set.objects.filter(lift=self.squat).count() == 5

    def test_import_with_other_data(self):
        Set.objects.create(lift=self.bench, weight_kg=100, reps=10, date='2014-01-01',
                           user=self.user)
        import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.good_mapping)
        assert Set.objects.filter(lift=self.bench).count() == 5

    def test_import_with_bad_mapping(self):
        with self.assertRaises(ValueError):
            import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.bad_mapping)
        assert Set.objects.filter(lift=self.bench).count() == 0

    def test_bad_data_doesnt_overwrite(self):
        # good db then bad db, should fail without screwing up existing data
        import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.good_mapping)
        with self.assertRaises(ValueError):
            import_fitnotes_db('fitnotes/testdata/example.fitnotes', self.user, self.bad_mapping)
        assert Set.objects.count() == 9
