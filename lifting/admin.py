from django.contrib import admin
from .models import Set


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    readonly_fields = ('user', 'lift', 'date')
    list_filter = ('user__username', 'lift')
    fields = ('user', 'lift', 'date', 'weight_kg', 'reps', 'source')
