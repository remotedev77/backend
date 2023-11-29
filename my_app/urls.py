from django.urls import path, re_path, include
from my_app.views import questions_views, statistic_views, test_views


urlpatterns = [
    path('get-questions/', questions_views.GetQuestionAPIView.as_view()),
    path('check-question/', questions_views.CheckMarafonQuestion.as_view()),
    path('get-user-statistic/', statistic_views.GetUserStatistic.as_view()),
    path('check-simulyator/', questions_views.CheckExamAPIView.as_view()),
    path('check-final-tets/', questions_views.CheckFinalTestAPIView.as_view()),
    path('check-category-question/', questions_views.CheckCategoryQuestionAPIView.as_view()),
    path('get-category-question/<str:category_name>/', questions_views.GetQuestionByCategory.as_view()),
    path('complie-questions/', test_views.GetComplieQuestionAPIView.as_view()),
    path('complie-test-questions/', test_views.GetComplieTestQuestionAPIView.as_view())
]
