from django.urls import path, re_path, include
from admin_app.views import questions_views, user_views


urlpatterns = [
    path('get-all-questions/', questions_views.GetAllQuestionAdminAPIView.as_view()),
    path('chage-question/<int:id>/', questions_views.ChangeQuestionAdminAPIView.as_view()),
    path('create-question/', questions_views.CreateQuestionAdminAPIView.as_view()),
    path('change-user/<int:id>/', user_views.ChangeUserAPIView.as_view()),
    path('create-user/', user_views.CreateUserAdminAPIView.as_view())
]