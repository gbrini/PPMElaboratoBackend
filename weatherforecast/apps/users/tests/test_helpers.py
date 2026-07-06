from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

PASSWORD = 'Password123!'

def create_user(username: str = 'testuser', role: str = 'standard'):
    user = User.objects.create_user(username=username, password=PASSWORD)
    user.role = role
    user.save()

    return user

def create_superuser(username: str = 'admin'):
    user = User.objects.create_superuser(username=username, password=PASSWORD)
    user.role = 'admin'
    user.save()

    return user