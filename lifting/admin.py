from django.contrib import admin
from .models import Exercise, Set

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    readonly_fields = ('user', 'exercise', 'date')
    list_filter = ('user__username', 'exercise')
    fields = ('user', 'exercise', 'date', 'weight_kg', 'reps', 'source')

