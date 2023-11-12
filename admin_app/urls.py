from django.urls import path, re_path, include
from admin_app.views import questions_views, user_views, answers_views


urlpatterns = [
    path('get-all-questions/', questions_views.GetAllQuestionAdminAPIView.as_view()),
    path('chage-question/<int:question_id>/', questions_views.ChangeQuestionAdminAPIView.as_view()),
    path('create-question/', questions_views.CreateQuestionAdminAPIView.as_view()),
    path('upload-csv-question-file/', questions_views.CreateQusetionFromCSVAPIView.as_view()),

    path('get-all-answers/', answers_views.GetAllAnswerAdminAPIView.as_view()),
    path('chage-answer/<int:answer_id>/', answers_views.ChangeAnswerAdminAPIView.as_view()),
    path('create-answer/', answers_views.CreateAnswerAdminAPIView.as_view()),

    path('change-user/<int:user_id>/', user_views.ChangeUserAPIView.as_view()),
    path('delete-user/<int:user_id>/', user_views.ChangeUserAPIView.as_view()),
    path('create-user/', user_views.CreateUserAdminAPIView.as_view()),
    path('get-users/', user_views.GetAllUserAPIView.as_view()),
    path('upload-csv-user-file/', user_views.CreateUserFromCSVAPIView.as_view()),
    path('get-user/', user_views.GetAdminUserAPIView.as_view()),
    path('create-manager-user/', user_views.CreateManagerOrSuperUserAPIView.as_view())
]