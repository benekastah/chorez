from django.contrib import admin
from django import forms
from django.db import models

from chorez.scheduler.models import Person, Chore


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput}
    }


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput}
    }
