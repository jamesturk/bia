from django.shortcuts import render
from django import forms


class FitnotesUploadForm(forms.Form):
    file = forms.FileField()


def fitnotes_upload(request):
    if request.method == 'POST':
        form = FitnotesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
    else:
        form = FitnotesUploadForm()
    return render(request, 'upload.html', {'form': form})
