from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='问题')
    pub_date = models.DateTimeField(verbose_name='发布日期')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1, verbose_name='作者')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '刚刚发布?'

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='问题')
    choice_text = models.CharField(max_length=200, verbose_name='选项')
    votes = models.IntegerField(default=0, verbose_name='投票')

    def __str__(self):
        return self.choice_text
