from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, verbose_name='评论类型')
    object_id = models.PositiveIntegerField(verbose_name='评论对象编号')
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING, verbose_name='评论发布者')

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING, verbose_name='根回复对象')
    parent = models.ForeignKey('self', related_name='parent_name',null=True,  on_delete=models.DO_NOTHING, verbose_name='评论归属')
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING, verbose_name='回复给')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']
