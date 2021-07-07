from django import forms

from . import models


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        widgets = {
            'password': forms.PasswordInput(),
        }
