from django.urls import path, re_path, include
from admin_app.views import answers_views


urlpatterns = [
    path('', answers_views.GetAllAnswerAdminAPIView.as_view()),
    path('<int:answer_id>/', answers_views.ChangeAnswerAdminAPIView.as_view()),
    # path('', answers_views.CreateAnswerAdminAPIView.as_view()),
    path('delete-multi-answers/', answers_views.DeleteAnswerAdminAPIView.as_view()),

]