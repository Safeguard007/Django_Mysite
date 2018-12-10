from django.contrib import admin
from .models import Blog, BlogType


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'id')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'blog_type', 'get_read_num', 'created_time', 'last_updated_time', 'id')

