from django.urls import path
from admin_app.views import company_views


urlpatterns = [
    path('', company_views.CompanyListCreateView.as_view(), name='company-list-create'),
    path('<int:pk>/', company_views.CompanyRetrieveUpdateDestroyView.as_view(), name='company-retrieve-update-destroy')

]