import datetime
import os
import tempfile
import calendar
from collections import defaultdict

from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import dates

from . import importers
from .models import Set


@login_required
def month(request, year, month):
    year, month = int(year), int(month)

    sets_by_day = defaultdict(list)
    for workset in Set.objects.filter(user=request.user, date__year=year, date__month=month):
        sets_by_day[workset.date.day].append(workset)
    date = datetime.date(year, month, 1)
    first_day, max_days = calendar.monthrange(year, month)
    # make first_day use 0 for sunday
    first_day = (first_day + 1) % 7

    # start calendar with a few blank days
    days = [None]*first_day

    for day in range(max_days+1):
        days.append({'number': day, 'sets': sets_by_day[day]})

    days_by_week = [days[0:7], days[7:14], days[14:21], days[21:28], days[28:35]

    return render(request, 'month.html', { 'date': date,
                                          'days': days_by_week
                                          })


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
    return render(request, 'upload.html', {'form': form})
