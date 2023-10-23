from rest_framework.pagination import PageNumberPagination

class QuestionPagination(PageNumberPagination):
    page_size = 5  # Set your desired page size
    page_size_query_param = 'page_size'  # Define the query parameter to allow clients to specify the page size
    page_query_param = 'page'  # Define the query parameter for specifying the current page
    last_page_strings = ('last',)  # Optionally, you can customize the query parameter used to request the last page