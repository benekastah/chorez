from django import forms

from chorez.scheduler.models import Chore


class ChoreForm(forms.ModelForm):

    name = forms.CharField()

    class Meta:
        model = Chore
        fields = [
            'name',
            'last_done',
            'duration',
            'frequency',
            'weekends_only',
            'blocked_by'
        ]


class ChoreMarkDoneForm(forms.ModelForm):

    class Meta:
        model = Chore
        fields = [
            'last_done',
            'snoozed_until'
        ]
