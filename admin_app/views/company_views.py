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

    def get(self, request, *args, **kwargs):
        if 'page' not in request.query_params:
            # Disable pagination if 'page' is not present
            self.pagination_class = None
        return self.list(request, *args, **kwargs)
    
    
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