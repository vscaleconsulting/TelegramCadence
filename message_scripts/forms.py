from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms

from . import models


class MessageScriptModelForm(forms.ModelForm):
    class Meta:
        model = models.MessageScript

        fields = (
            "message",
            "account",
            "time_days",
            "time_hours",
            "time_minutes",
            "time_seconds",
        )

        widgets = {
            "message": forms.Textarea(attrs={"Placeholder": "Message", 'autofocus': 'autofocus'}),
            "account": forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            "message": ""
        }
