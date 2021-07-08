from django.contrib import admin

from . import models


@admin.register(models.MessageScript)
class MessageScriptModelAdmin(admin.ModelAdmin):
    list_display = ('cadence',
                    'account',
                    'message',
                    'time_days',
                    'time_hours',
                    'time_minutes',
                    'time_seconds')
