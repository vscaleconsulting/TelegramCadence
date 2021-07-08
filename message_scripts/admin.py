from django.contrib import admin

from . import models


@admin.register(models.MessageScript)
class MessageScriptModelAdmin(admin.ModelAdmin):
    list_display = ('cadence',
                    'account',
                    )
