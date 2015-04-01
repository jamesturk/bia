from django.test import TestCase
from lifting.models import Exercise, Set
from lifting.importers import import_fitnotes_db


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

    def test_basic_import(self):
        # ensure that the data comes in
        import_fitnotes_db('lifting/testdata/example.fitnotes')

        assert Exercise.objects.count() == 2
        bp = Exercise.objects.get(names__contains=["flat barbell bench press"])
        squat = Exercise.objects.get(names__contains=["barbell squat"])
        assert Set.objects.count() == 9

    def test_double_import(self):
        # two identical dbs, should be idempotent
        import_fitnotes_db('lifting/testdata/example.fitnotes')
        import_fitnotes_db('lifting/testdata/example.fitnotes')
        assert Exercise.objects.count() == 2
        assert Set.objects.count() == 9

    def test_bad_import(self):
        # good db then bad db, should fail without screwing up existing data
        import_fitnotes_db('lifting/testdata/example.fitnotes')
        with self.assertRaises(Exception):
            # baddata.fitnotes has all exercise ids set to 9999
            import_fitnotes_db('lifting/testdata/baddata.fitnotes')
        assert Exercise.objects.count() == 2
        assert Set.objects.count() == 9
