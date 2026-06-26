from django.shortcuts import render
from rest_framework.views import APIView
#from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class RegisterView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer