from django.urls import path, re_path
from . import views


app_name = 'blog'
urlpatterns = [
    re_path(r'^$', views.get_blog_list, name='blog_list'),
    re_path(r'^(?P<blog_id>[0-9]+)/$', views.get_blog_detail, name='blog_detail'),
    re_path(r'^type/(?P<blog_type_id>[0-9]+)/$', views.get_blog_list_type, name='blog_list_type'),
    re_path(r'^date/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.get_blog_list_date, name='blog_list_date')
]
