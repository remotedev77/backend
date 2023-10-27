from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
class QuestionPagination(PageNumberPagination):
    page_size = 2  # Set your desired page size
    page_size_query_param = 'page_size'  # Define the query parameter to allow clients to specify the page size
    page_query_param = 'page'  # Define the query parameter for specifying the current page
    last_page_strings = ('last',)  # Optionally, you can customize the query parameter used to request the last page

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))