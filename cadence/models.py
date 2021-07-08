from django.db import models

from core import models as core_models
from users import models as user_models


class Cadence(core_models.TimeStampedModel):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
