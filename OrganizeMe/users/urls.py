from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]