from django.db import models

from accounts import models as account_models
from cadence import models as cadence_models
from core import models as core_models


class MessageScript(core_models.TimeStampedModel):
    cadence = models.ForeignKey(cadence_models.Cadence, on_delete=models.CASCADE)
    account = models.ForeignKey(account_models.Account, on_delete=models.CASCADE)
    message = models.TextField()
    time_days = models.PositiveIntegerField(default=0)
    time_hours = models.IntegerField(choices=((i, i) for i in range(24)), default=0)
    time_minutes = models.IntegerField(choices=((i, i) for i in range(60)), default=0)
    time_seconds = models.IntegerField(choices=((i, i) for i in range(60)), default=0)
