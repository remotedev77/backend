from django.urls import path, re_path, include
from admin_app.views import questions_views


urlpatterns = [
    path('get-all-admin-questions/', questions_views.GetAllQuestionAdminAPIView.as_view()),

]