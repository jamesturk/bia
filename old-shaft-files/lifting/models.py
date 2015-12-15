

class Plan(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(PlanTag, related_name='plans')
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='plans', null=True)
    cloned_from = models.ForeignKey('self', null=True)

    objects = ByNameManager()

    def __str__(self):
        return '{0}'.format(self.name)

    def get_absolute_url(self):
        return reverse('lifting.views.plan', args=[str(self.id)])

    def natural_key(self):
        return (self.name,)

    def get_days(self, user):
        exercise_rules = {}
        days = []
        for day in self.days.all():
            day_sets = []
            for exercise in day.exercises.all():
                for reps in exercise.get_sets():
                    rules = exercise_rules.setdefault(exercise.exercise,
                                                      exercise.exercise.rules.get(user=user))
                    day_sets.append(
                        Set(exercise=exercise.exercise,
                            weight=round_to(rules.work_weight*exercise.percent, rules.increment),
                            reps=reps,
                            type='planned')
                    )
                    if exercise.raise_weight:
                        rules.work_weight += rules.increment
            days.append(day_sets)
        return days


class PlanDay(models.Model):
    plan = models.ForeignKey(Plan, related_name='days')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return '{0}: {1}'.format(self.plan, self.name)

    class Meta:
        ordering = ['order']


class PlanExercise(models.Model):
    plan_day = models.ForeignKey(PlanDay, related_name='exercises')
    exercise = models.ForeignKey(Exercise)
    order = models.PositiveIntegerField()
    sets = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=4, decimal_places=3, default=1)
    raise_weight = models.BooleanField(default=False)

    def get_sets(self):
        return [int(s) for s in self.sets.split(',')]

    def get_set_display(self):
        sets = []
        last_reps = None
        last_reps_num = 0
        for s in self.get_sets():
            if last_reps and s != last_reps:
                sets.append('{0}x{1}'.format(last_reps_num, last_reps))
                last_reps_num = 0
            last_reps_num += 1
            last_reps = s
        sets.append('{0}x{1}'.format(last_reps_num, last_reps))
        return ', '.join(sets)

    def get_percent_display(self):
        return '{0:%}'.format(self.percent)

    class Meta:
        ordering = ['order']
