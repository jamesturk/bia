from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required


@login_required
def edit_profile(request):
    form = request.user.profile

    return render(request, 'profiles/edit.html', {'form': form})
