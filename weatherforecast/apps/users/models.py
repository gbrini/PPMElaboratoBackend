from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .constants import ROLE_CHOICES

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='standard')

    def getMaximumRequestsNumber(self):
        return settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'][self.role]

    def __str__(self):
        return self.username