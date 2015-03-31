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
    import_fitnotes_db('example.fitnotes')

    #assert Exercise.objects.count() == 2

    bp = Exercise.objects.get(name="bench press")
    squat = Exercise.objects.get(name="barbell squat")

    assert Set.objects.count() == 9
