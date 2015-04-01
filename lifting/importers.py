import sqlite3
from lifting.models import Exercise, Set


def _clean_name(name):
    return name.lower()


def import_fitnotes_db(filename):
    # exercise names to db ids
    exercises = {_clean_name(e.name): e.id for e in Exercise.objects.all()}

    # build mapping FitNotes exercise id => our exercise id
    exercise_id_mapping = {}

    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    for fnid, ename in cur.execute('SELECT _id, name FROM exercise WHERE exercise_type_id=0'):
        cleaned = _clean_name(ename)
        # map to an Exercise id or str
        exercise_id_mapping[fnid] = exercises[cleaned] if cleaned in exercises else cleaned

    for fnid, date, weight_kg, reps in cur.execute(
        'SELECT exercise_id, date, metric_weight, reps FROM training_log'):

        # create Exercise if it wasn't found and there's a workout using it
        if isinstance(exercise_id_mapping[fnid], str):
            exercise_id_mapping[fnid] = Exercise.objects.create(name=exercise_id_mapping[fnid]).id

        exercise_id = exercise_id_mapping[fnid]

        Set.objects.create(exercise_id=exercise_id, date=date, weight_kg=weight_kg, reps=reps)
