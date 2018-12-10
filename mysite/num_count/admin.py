from django.contrib import admin
from .models import ReadNum, ReadNumDate


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'read_num')


@admin.register(ReadNumDate)
class ReadNumDateAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'read_date', 'read_num')
