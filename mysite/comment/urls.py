from django.urls import path
from . import views


urlpatterns = [
    path('upload_comment', views.upload_comment, name='upload_comment')
]
