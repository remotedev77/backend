from django.urls import path, re_path, include
from users.views import users_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', users_views.LoginUserApi.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', users_views.RegisterAPIView.as_view(), name="sign_up"),
    path('user/', users_views.GetUserAPIView.as_view(), name = 'get_user'),
    path('user-questions/', users_views.UserStatisticQuestionAPIView.as_view())
]
