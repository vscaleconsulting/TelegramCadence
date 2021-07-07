from django.contrib import admin

from . import models


@admin.register(models.Account)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('acc_name', 'acc_id', 'user')



