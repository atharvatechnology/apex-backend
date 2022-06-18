from rest_framework import pagination
from rest_framework.response import responses


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10000


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return responses.Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
            }
        )
