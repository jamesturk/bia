import calendar
import datetime
import decimal
import os
import tempfile
from collections import defaultdict, Counter

from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import dates
from django.db.models import Count, Max

from inventory.models import Lift, Bar
from .models import Set
from .forms import LiftingOptionsForm


@login_required
def month_lifts(request, year, month):
    year, month = int(year), int(month)

    sets_by_day = defaultdict(set)
    for workset in Set.objects.filter(user=request.user, date__year=year, date__month=month):
        sets_by_day[workset.date.day].add(workset.lift)
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
    lifts = Lift.objects.filter(sets__user=request.user).annotate(
        total=Count('sets'), max_kg=Max('sets__weight_kg'),
        last_date=Max('sets__date'),
    ).order_by('-last_date')
    return render(request, 'lifting/lift_list.html', {'lifts': lifts})


@login_required
def by_lift(request, lift_id):
    lift = Lift.objects.get(pk=lift_id)
    sets = Set.objects.filter(user=request.user, lift=lift).order_by('-date')
    return render(request, 'lifting/by_lift.html', {'lift': lift, 'sets': sets})


@login_required
def edit_options(request):
    lifting_options = request.user.lifting_options

    if request.method == 'POST':
        print(request.POST)
        plates = []
        for weight, number in zip(request.POST.getlist('plate_weight'),
                                  request.POST.getlist('plate_number')):
            if weight and number:
                plates += [decimal.Decimal(weight)] * int(number)

        lifting_options.plate_pairs = plates
        lifting_options.default_bar_id = int(request.POST.get('barbell'))
        lifting_options.lifting_units = request.POST.get('lifting_units')
        lifting_options.save()

    bars = Bar.objects.all()
    plates = sorted(Counter(lifting_options.plate_pairs).items())

    return render(request, 'profiles/edit.html', {'lifting_options': lifting_options,
                                                  'bars': bars, 'plates': plates,
                                                 })
