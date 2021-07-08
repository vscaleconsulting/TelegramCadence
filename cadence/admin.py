from django.contrib import admin

from . import models


@admin.register(models.Cadence)
class CadenceModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
