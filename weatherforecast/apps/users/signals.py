from django.db.models.signals import pre_save
from django.dispatch import receiver
#from django.contrib.auth.models import User
from .models import CustomUser

@receiver(pre_save, sender=CustomUser)
def set_user_permissions(sender, instance, **kwargs):
    if instance.role == 'admin':
        instance.is_staff = True
        instance.is_superuser = True
    else:
        instance.is_staff = False
        instance.is_superuser = False