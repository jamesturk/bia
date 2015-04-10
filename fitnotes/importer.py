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

    # build mapping FitNotes exercise id => our lift id
    lift_id_mapping = {}

    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    for fnid, ename in cur.execute('SELECT _id, name FROM exercise WHERE exercise_type_id=0'):
        cleaned = _clean_name(ename)

        if cleaned not in fitnotes_to_lift:
            lift_id_mapping[fnid] = cleaned
        else:
            lift_id_mapping[fnid] = lift_ids[fitnotes_to_lift[cleaned]]

    with transaction.atomic():
        Set.objects.filter(source='fitnotes').delete()
        for fnid, date, weight_kg, reps in cur.execute(
            'SELECT exercise_id, date, metric_weight, reps FROM training_log'):

            # error if mapping wasn't found and there's a workout using it
            if isinstance(lift_id_mapping[fnid], str):
                raise ValueError('no known conversion for fitnotes exercise "{}"'.format(
                    lift_id_mapping[fnid]))

            lift_id = lift_id_mapping[fnid]

            Set.objects.create(lift_id=lift_id, date=date, weight_kg=weight_kg, reps=reps,
                               source='fitnotes', user=user)
