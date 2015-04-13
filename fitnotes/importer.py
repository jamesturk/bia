import sqlite3
from django.db import transaction
from lifting.models import Lift, Set


DEFAULT_MAPPING = {
    'flat barbell bench press': 'barbell bench press',
    'barbell curl': 'barbell curl',
    'deadlift': 'barbell deadlift',
    'barbell squat': 'barbell squat',
    'overhead press': 'standing overhead press',
    'barbell front squat': 'barbell front squat',
    'barbell row': 'barbell row',
    'pull up': 'pull up',
    'chin up': 'chin up',
    'push up': 'push up',
    'dumbbell curl': 'dumbbell curl',
}


def _clean_name(name):
    return name.lower()


def import_fitnotes_db(filename, user, fitnotes_to_lift=DEFAULT_MAPPING):
    # lift name => id
    lift_ids = {_clean_name(l.name): l.id for l in Lift.objects.all()}

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    with transaction.atomic():
        Set.objects.filter(source='fitnotes').delete()
        count = 0
        for fname, date, weight_kg, reps in cur.execute(
            'SELECT name, date, metric_weight, reps FROM training_log, exercise '
            'WHERE exercise_type_id=0 and exercise_id=exercise._id'
        ):

            try:
                lift_id = lift_ids[fitnotes_to_lift[_clean_name(fname)]]
            except KeyError:
                raise ValueError('no known conversion for fitnotes exercise "{}"'.format(fname))

            Set.objects.create(lift_id=lift_id, date=date, weight_kg=weight_kg, reps=reps,
                               source='fitnotes', user=user)
            count += 1

    return count
