from django.urls import path
from . import views

app_name = 'user_accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('user-panel/', views.user_panel_view, name='user_panel'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
]
