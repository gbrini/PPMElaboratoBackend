from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserListSerializer, UserRoleSerializer
from .permissions import IsAdminUser

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserListView(APIView):
    permission_classes = [ IsAdminUser ]

    def get(self, request):
        users = CustomUser.objects.all()

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(users, request)

        output_serializer = UserListSerializer(result_page, many=True, context = { "request": request })

        return paginator.get_paginated_response(output_serializer.data)

class UserDetailView(APIView):
    permission_classes = [ IsAdminUser ]

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