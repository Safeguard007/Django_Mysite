from django.contrib import admin
from .models import LikeCount, LikeRecord


# @admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'content_object', 'like_num')


# @admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'content_object', 'user', 'like_time')
