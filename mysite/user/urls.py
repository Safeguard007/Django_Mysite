from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('login_modal/', views.login_modal, name='login_modal'),
    path('register/', views.user_register, name='user_register'),
    path('user_inf/', views.user_inf, name='user_inf'),
]
