from decimal import Decimal as D
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required
from .models import UserSettings, ExerciseRules, Exercise, Plan
from .forms import UserSettingsForm, PlanForm



@require_http_methods(["GET", "POST"])
@login_required
def plan_edit(request, id):
    """ edit details of a plan """
    plan = get_object_or_404(Plan, pk=id)
    exercises = Exercise.objects.all()
    if request.method == 'GET':
        pform = PlanForm(instance=plan)
    return render(request, 'lifting/plan_edit.html',
                  {'pform': pform, 'plan': plan, 'exercises': exercises})


@require_http_methods(["GET", "POST"])
@login_required
def rules(request):
    """ a view that allows a user to view/edit their list of rules """
    gr, _ = UserSettings.objects.get_or_create(user=request.user)
    ers = list(ExerciseRules.objects.filter(user=request.user))
    exercises = Exercise.objects.exclude(id__in=[er.exercise_id for er in ers])
    if request.method == 'GET':
        grform = UserSettingsForm(instance=gr)
    elif request.method == 'POST':
        grform = UserSettingsForm(request.POST, instance=gr)
        if grform.is_valid():
            grform.save()
        for exercise, start, inc, work in zip(request.POST.getlist('er.exercise'),
                                              request.POST.getlist('er.start_weight'),
                                              request.POST.getlist('er.increment'),
                                              request.POST.getlist('er.work_weight')):
            exercise = int(exercise)
            start = D(start)
            inc = D(inc)
            work = D(work)

            er, _ = ExerciseRules.objects.get_or_create(user=request.user,
                                                        exercise_id=int(exercise))
            er.start_weight = start
            er.increment = inc
            er.work_weight = work
            er.save()
    return render(request, 'lifting/rules.html',
                  {'grform': grform, 'exercise_rules': ers, 'exercises': exercises, })


def er_row(request, eid):
    return render(request, 'lifting/_er-row.html',
                  {'er': ExerciseRules(user=request.user, exercise=Exercise.objects.get(pk=eid))})
