from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login_modal/', views.login_modal, name='login_modal'),
    path('register/', views.user_register, name='user_register'),
    path('user_inf/', views.user_inf, name='user_inf'),
    path('change_profile/', views.change_proflie, name='change_profile'),
    path('blind_email/', views.blind_email, name='blind_email'),
    path('blind_email_code/', views.send_verification_code, name='send_verification_code'),
]
