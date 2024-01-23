from django.urls import path
from admin_app.views import direction_views


urlpatterns = [
    path('', direction_views.DirectionListAPIView.as_view()),
    

]