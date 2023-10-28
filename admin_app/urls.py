from django.urls import path, re_path, include
from admin_app.views import questions_views


urlpatterns = [
    path('get-all-questions/', questions_views.GetAllQuestionAdminAPIView.as_view()),
    path('chage-question/<int:id>/', questions_views.ChangeQuestionAdminAPIView.as_view())
]