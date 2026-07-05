from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserListSerializer
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