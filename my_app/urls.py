from django.urls import path, re_path, include
from my_app.views import questions_views, statistic_views


urlpatterns = [
    path('get-questions/', questions_views.GetQuestionAPIView.as_view()),
    path('check-question/', questions_views.CheckQuestion.as_view()),
    path('get-user-statistic/', statistic_views.GetUserStatistic.as_view()),
    path('check-simulyator/', questions_views.CheckExamAPIView.as_view()),
    path('get-category-question/<str:category_name>/', questions_views.GetQuestionByCategory.as_view())
]
