from django import forms

from . import models


class CadenceModelForm(forms.ModelForm):
    class Meta:
        model = models.Cadence

        fields = (
            "name",
        )

        # account = forms.ModelMultipleChoiceField(queryset=)

        widgets = {
            "name": forms.TextInput(attrs={"Placeholder": "Enter Cadence Name", 'autofocus': 'autofocus'}),
        }

        labels = {
            "name": ""
        }


class ExecuteCadenceForm(forms.Form):
    global_time = forms.DateTimeField()
    grp_name = forms.CharField(max_length=255)
