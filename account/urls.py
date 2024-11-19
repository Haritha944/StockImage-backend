from django.urls import path
from .views import RegisterView,LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]