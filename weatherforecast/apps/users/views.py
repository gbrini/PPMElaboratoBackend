from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserListSerializer, UserRoleSerializer, UserThrottleProfileSerializer, ChangePasswordSerializer
from .permissions import IsAdminUser
from .throttles import RoleBasedThrottle

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    throttle_classes = []

class UserListView(APIView):
    permission_classes = [ IsAdminUser ]
    throttle_classes = []

    def get(self, request):
        users = CustomUser.objects.all().order_by('id')

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(users, request)

        output_serializer = UserListSerializer(result_page, many=True, context = { "request": request })

        return paginator.get_paginated_response(output_serializer.data)

class UserDetailView(APIView):
    permission_classes = [ IsAdminUser ]
    throttle_classes = []

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        user.delete()

        return Response({ "message": "User deleted successfully!" }, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        serializer = UserRoleSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = [ IsAuthenticated ]
    throttle_classes = []

    def get(self, request):
        throttle = RoleBasedThrottle()
        throttle.configure(request)

        if throttle.key is None:
            throttle_info = {
                "rate": "Unlimited",
                "limit": None,
                "remaining": None,
                "reset_in": None,
            }
        else:
            history = cache.get(throttle.key, [])
            now = throttle.timer()

            history = [
                timestamp
                for timestamp in history
                if timestamp > now - throttle.duration
            ]

            limit = throttle.num_requests
            remaining = max(0, limit - len(history))

            reset_in = (
                max(0, int(history[-1] + throttle.duration - now))
                if history
                else 0
            )

            throttle_info = {
                "rate": throttle.rate,
                "limit": limit,
                "remaining": remaining,
                "reset_in": reset_in,
            }

        data = {
            "username": request.user.username,
            "role": request.user.role,
            "throttle": throttle_info,
        }

        serializer = UserThrottleProfileSerializer(data)
        
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [ IsAuthenticated ]
    throttle_classes = []

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({ "error": "Wrong password" }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({ "message": "Password update successfully" })