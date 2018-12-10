from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from num_count.models import GetReadNum


class BlogType(models.Model):
    type_name = models.CharField(max_length=10, verbose_name='类型名称')

    def __str__(self):
        return self.type_name


class Blog(models.Model, GetReadNum):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='作者')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name='文章类型')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='修改日期')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
