from rest_framework.pagination import PageNumberPagination


class CustomNumberPagination(PageNumberPagination):
    """
    Custom pagination class based on PageNumberPagination in Django Rest Framework.

    This class extends the default PageNumberPagination and customizes the pagination
    settings for a specific use case.

    Attributes:
    - page_size (int): The number of items to include on each page. Defaults to 5.
    - page_size_query_param (str): The query parameter to determine the page size.
                                  Defaults to "page_size".
    - max_page_size (int): The maximum allowed value for the page size. Defaults to 15.
    - page_query_param (str): The query parameter to determine the requested page number.
                            Defaults to "page".
    """

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 15
    page_query_param = "page"
