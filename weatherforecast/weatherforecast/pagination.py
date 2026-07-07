from rest_framework.pagination import PageNumberPagination
from django.conf import settings

class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.MY_PROJECT_SETTINGS['PAGE_SIZE']
    page_size_query_param = 'page_size'
    max_page_size = settings.MY_PROJECT_SETTINGS['MAX_PAGE_SIZE']