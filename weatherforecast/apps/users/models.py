from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ( 'standard', 'Standard' ),
        ( 'premium', 'Premium' ),
        ( 'admin', 'Admin' )
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='standard')

    def getMaximumRequestsNumber(self):
        return settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'][self.role]

    def __str__(self):
        return self.username