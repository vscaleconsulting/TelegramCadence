from django import forms

from . import models
from core import functions


# class AccountModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Account
#         fields = (
#             "acc_name",
#         )
# 
#         widgets = {
#             "acc_name": forms.TextInput(attrs={"Placeholder": "Account Name", 'autofocus': 'autofocus'})
#         }
# 
#         labels = {
#             "acc_name": ""
#         }
# 
#     def clean(self):
#         acc_name = self.cleaned_data['acc_name']
#         acc_name = acc_name.lstrip('@')
#         acc_id = functions.get_uid(acc_name)
#         already_user = models.Account.objects.filter(acc_name=acc_name)
#         if already_user:
#             raise forms.ValidationError('This Account Already Exists.')
#         try:
#             int(list(acc_id.values())[0])
#             if 'group' in acc_id.keys():
#                 raise forms.ValidationError('This ID belongs to a Telegram Group.')
#         except AttributeError:
#             raise forms.ValidationError(acc_id)
#         self.cleaned_data['acc_id'] = acc_id['user']
# 
#         return self.cleaned_data


