from django.urls import path
from admin_app.views import user_views


urlpatterns = [
    path('', user_views.GetAllUserAPIView.as_view()),
    path('<int:user_id>/', user_views.ChangeUserAPIView.as_view()),
    # path('create-user/', user_views.CreateUserAdminAPIView.as_view()),
    path('current/', user_views.GetAdminUserAPIView.as_view()),
    path('upload-csv-user-file/', user_views.CreateUserFromCSVAPIView.as_view()),
    # path('<int:user_id>/', user_views.GetUserForAdminAPIView.as_view()),
    path('statistics/<int:user_id>/', user_views.GetUserStatistic.as_view()),
]