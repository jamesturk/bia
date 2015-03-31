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
        if cleaned in exercises:
            exercise_id_mapping[fnid] = exercises[cleaned]

    for fnid, date, weight_kg, reps in cur.execute(
        'SELECT exercise_id, date, metric_weight, reps FROM training_log'):

        # create Exercise if it wasn't found and there's a workout using it
        if fnid not in exercise_id_mapping:
            exercise_id_mapping[fnid] = Exercise.objects.create(name=cleaned).id

        exercise_id = exercise_id_mapping[fnid]

        Set.objects.create(exercise_id=exercise_id, date=date, weight_kg=weight_kg, reps=reps)
