from django.urls import path, re_path, include
from admin_app.views import questions_views


urlpatterns = [
    path('', questions_views.GetAllQuestionAdminAPIView.as_view()),
    path('<int:question_id>/', questions_views.ChangeQuestionAdminAPIView.as_view()),
    path('upload-csv-question-file/', questions_views.CreateQusetionFromCSVAPIView.as_view()),

]
