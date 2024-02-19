from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

from rest_framework import generics
from rest_framework.response import Response
from admin_app.serializers.company_serializers import CompanySerializer
from admin_app.permissions import IsAdminOrSuperUser
from admin_app.pagination import CompanyPagination
from users.models import Company

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrSuperUser]
    pagination_class = CompanyPagination
    @swagger_auto_schema(
            manual_parameters=[
                
                openapi.Parameter(
                    'search',
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_STRING,
                )
            ],responses={200: CompanySerializer},
    )
    def get(self, request, *args, **kwargs):
        if 'page' not in request.query_params:
            # Disable pagination if 'page' is not present
            self.pagination_class = None
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        filters = Q()
        
        if search_query:
            filters |= Q(company_name__icontains=search_query)

        queryset = queryset.filter(filters)
        return queryset
    
class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrSuperUser]

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)