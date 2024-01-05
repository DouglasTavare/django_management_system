from rest_framework.pagination import PageNumberPagination

class CustomNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 15
    page_query_param = 'page'