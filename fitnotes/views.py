import os
import tempfile
from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import importer

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
                importer.import_fitnotes_db(fname, request.user)
            finally:
                os.remove(fname)
    else:
        form = FitnotesUploadForm()
    return render(request, 'lifting/fitnotes.html', {'form': form})
