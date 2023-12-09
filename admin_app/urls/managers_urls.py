from django.urls import path
from admin_app.views import user_views


urlpatterns = [
    path('', user_views.ManagerListCreateView.as_view()),
    path('<int:pk>/',user_views.ManagerRetrieveUpdateDestroyView.as_view())
]

# path('', user_views.CreateManagerOrSuperUserAPIView.as_view()),