from decimal import Decimal as D
from .models import ExerciseRules, Set
from .utils import round_to


def warmup_ss(exercise, weight, user):
    """
        Starting Strength Warmup
        ========================
        (start)x5 x2
        (40%)x5
        (60%)x3
        (80%)x2
    """

    # get relevant rules
    rules, _ = ExerciseRules.objects.get_or_create(user=user, exercise=exercise)
    start = rules.start_weight

    # empty bar sets
    sets = [Set(exercise=exercise, weight=start, reps=5, type='warmup')]*2

    if D('0.8')*weight < start:
        return []

    for reps, pct in ((5, D('0.4')), (3, D('0.6')), (2, D('0.8'))):
        ww = round_to(weight * pct, D('5'))
        if ww > start:
            sets.append(Set(exercise=exercise, weight=ww, reps=reps, type='warmup'))

    return sets
