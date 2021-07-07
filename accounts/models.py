from django.db import models

from core import models as core_models
from users import models as user_models


class Account(core_models.TimeStampedModel):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    acc_name = models.CharField(max_length=255)
    acc_username = models.CharField(max_length=255, null=True, blank=True)
    acc_id = models.IntegerField(unique=True)
    sess_str = models.TextField()
    phone = models.BigIntegerField()

    def __str__(self):
        return self.acc_name
