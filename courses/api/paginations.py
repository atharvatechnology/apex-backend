from rest_framework import pagination
from rest_framework.response import Response


# Custom pagination
class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "p"

    def get_paginated_response(self, data):
        response = Response(data)
        response["count"] = self.page.paginator.count
        response["next"] = self.get_next_link()
        response["previous"] = self.get_previous_link()
        return response
