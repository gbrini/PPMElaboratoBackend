from django.contrib.auth import get_user_model

User = get_user_model()

PASSWORD = 'password'

def create_user(username: str = 'testuser'):
    return User.objects.create_user(username=username, password=PASSWORD)

def create_superuser(username: str = 'admin'):
    user = User.objects.create_superuser(username=username, password=PASSWORD)
    user.role = 'admin'
    user.save()

    return user