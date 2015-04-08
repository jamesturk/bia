import datetime
import os
import tempfile
import calendar
from collections import defaultdict

from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import dates
from django.db.models import Count, Max

from . import importers
from .models import Set, Exercise


@login_required
def month_lifts(request, year, month):
    year, month = int(year), int(month)

    sets_by_day = defaultdict(set)
    for workset in Set.objects.filter(user=request.user, date__year=year, date__month=month):
        sets_by_day[workset.date.day].add(workset.exercise)
    date = datetime.date(year, month, 1)

    # build calendar
    first_day, max_days = calendar.monthrange(year, month)
    # alter first_day to use 0 for sunday
    first_day = (first_day + 1) % 7

    # start calendar with a few blank days, then put days into array
    days = [None]*first_day
    for day in range(1, max_days+1):
        days.append({'number': day, 'lifts': sets_by_day[day]})

    # split days up into weeks
    days_by_week = [days[0:7], days[7:14], days[14:21], days[21:28], days[28:35], days[35:42]]

    # prev and next month
    if date.month == 1:
        prev_date = datetime.date(year-1, 12, 1)
        next_date = datetime.date(year, 2, 1)
    elif date.month == 12:
        prev_date = datetime.date(year, 11, 1)
        next_date = datetime.date(year+1, 1, 1)
    else:
        prev_date = datetime.date(year, month-1, 1)
        next_date = datetime.date(year, month+1, 1)

    return render(request, 'lifting/month.html', {'date': date, 'days': days_by_week,
                                                  'prev_date': prev_date, 'next_date': next_date
                                                 })

@login_required
def day_lifts(request, year, month, day):
    year, month, day = int(year), int(month), int(day)

    sets = list(Set.objects.filter(user=request.user, date__year=year, date__month=month,
                                   date__day=day))
    date = datetime.date(year, month, day)
    prev_date = date - datetime.timedelta(days=1)
    next_date = date + datetime.timedelta(days=1)

    return render(request, 'lifting/day.html', {'date': date, 'sets': sets,
                                                'prev_date': prev_date, 'next_date': next_date
                                               })


@login_required
def lift_list(request):
    lifts = Exercise.objects.filter(sets__user=request.user).annotate(
        total=Count('sets'), max_kg=Max('sets__weight_kg'),
        last_date=Max('sets__date'),
    ).order_by('-last_date')
    return render(request, 'lifting/lift_list.html', {'lifts': lifts})


@login_required
def by_lift(request, lift_id):
    lift = Exercise.objects.get(pk=lift_id)
    sets = Set.objects.filter(user=request.user, exercise=lift).order_by('-date')
    return render(request, 'lifting/by_lift.html', {'lift': lift, 'sets': sets})


class FitnotesUploadForm(forms.Form):
    file = forms.FileField()


@login_required
def fitnotes_upload(request):
    if request.method == 'POST':
        form = FitnotesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            _, fname = tempfile.mkstemp()
            with open(fname, 'wb') as tmp:
                for chunk in request.FILES['file'].chunks():
                    tmp.write(chunk)
            try:
                importers.import_fitnotes_db(fname, request.user)
            finally:
                os.remove(fname)
    else:
        form = FitnotesUploadForm()
    return render(request, 'lifting/fitnotes.html', {'form': form})
