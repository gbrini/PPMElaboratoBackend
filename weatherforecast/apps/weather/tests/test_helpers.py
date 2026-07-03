from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import UserSearchHistory

User = get_user_model()

PASSWORD = 'password'

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

def create_search_history(user, days_ago=0, count=1):
    timestamp = timezone.now() - timezone.timedelta(days=days_ago)
    return UserSearchHistory.objects.create(
        user=user,
        search_params={"location": "Rome"},
        result_count=count,
        timestamp=timestamp
    )