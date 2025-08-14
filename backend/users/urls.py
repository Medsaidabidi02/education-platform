from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='user-login'),
    path('logout/', views.logout_view, name='user-logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('sessions/', views.UserSessionListView.as_view(), name='user-sessions'),
    path('sessions/<int:session_id>/terminate/', views.terminate_session, name='terminate-session'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('health/', views.health_check, name='health-check'),
]