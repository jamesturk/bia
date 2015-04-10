from django.contrib import admin
from .models import Lift

@admin.register(Lift)
class LiftAdmin(admin.ModelAdmin):
    pass
