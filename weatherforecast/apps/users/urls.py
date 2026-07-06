from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserListView, UserDetailView, UserView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('list/', UserListView.as_view(), name='list_users'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail_user'),
    path('me', UserView.as_view(), name='me')
]