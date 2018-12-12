from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.cache import caches
from django.db.models import Count

from .models import Blog, BlogType
from num_count.utils import read_cookie, read_num_by_days, get_hot_blog
from comment.models import Comment
from comment.forms import CommentForm
from mysite.forms import LoginForm


# 获取各博客页面公共内容
def get_blog_base(blog_list):
    pass


# 获取几日内最热门博客
def get_hot_data():
    blog_content = ContentType.objects.get_for_model(Blog)
    today_hot = get_hot_blog(blog_content, 0)
    yesterday_hot = get_hot_blog(blog_content, 1)
    seven_day_hot = get_hot_blog(blog_content, 7)
    thirty_day_hot = get_hot_blog(blog_content, 30)

    return today_hot, yesterday_hot, seven_day_hot, thirty_day_hot


# 获取全部列表
def get_blog_list(request):
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 10)
    page_num = request.GET.get('page', 1)
    blog_page = paginator.get_page(page_num)
    today_hot, yesterday_hot, seven_day_hot, thirty_day_hot = get_hot_data()

    context = dict()
    context['today_hot_blogs'] = today_hot
    context['yesterday_hot_blogs'] = yesterday_hot
    context['seven_day_hot_blogs'] = seven_day_hot
    context['thirty_day_hot_blogs'] = today_hot
    context['user'] = request.user
    context['blogs'] = Blog.objects.all()
    context['blog_page'] = blog_page
    context['blog_type'] = BlogType.objects.annotate(blog_type_count=Count('blog'))
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render_to_response('blog/blog_list.html', context)


# 获取按类型分配列表
def get_blog_list_type(request, blog_type_id):
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    blog_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blog_list, 10)
    page_num = request.GET.get('page', 1)
    blog_page = paginator.get_page(page_num)
    today_hot, yesterday_hot, seven_day_hot, thirty_day_hot = get_hot_data()

    context = dict()
    context['today_hot_blogs'] = today_hot
    context['yesterday_hot_blogs'] = yesterday_hot
    context['seven_day_hot_blogs'] = seven_day_hot
    context['thirty_day_hot_blogs'] = today_hot
    context['user'] = request.user
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_page'] = blog_page
    context['blog_type'] = blog_type
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render_to_response('blog/blog_list_type.html', context)


# 获取按时间分配列表
def get_blog_list_date(request, year, month):
    blog_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    paginator = Paginator(blog_list, 10)
    page_num = request.GET.get('page', 1)
    blog_page = paginator.get_page(page_num)
    today_hot, yesterday_hot, seven_day_hot, thirty_day_hot = get_hot_data()

    context = dict()
    context['today_hot_blogs'] = today_hot
    context['yesterday_hot_blogs'] = yesterday_hot
    context['seven_day_hot_blogs'] = seven_day_hot
    context['thirty_day_hot_blogs'] = today_hot
    context['user'] = request.user
    context['blogs'] = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context['blog_page'] = blog_page
    context['blog_type'] = BlogType.objects.annotate(blog_type_count=Count('blog'))
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    context['blog_with_dates'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blog_list_date.html', context)


# 获取具体博客内容
def get_blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    read_key = read_cookie(request, blog)
    dates, read_nums = read_num_by_days(blog, days=7)
    today_hot, yesterday_hot, seven_day_hot, thirty_day_hot = get_hot_data()

    context = dict()
    context['today_hot_blogs'] = today_hot
    context['yesterday_hot_blogs'] = yesterday_hot
    context['seven_day_hot_blogs'] = seven_day_hot
    context['thirty_day_hot_blogs'] = today_hot
    context['login_form'] = LoginForm()
    context['user'] = request.user
    context['blog'] = blog
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    response = render_to_response('blog/blog_detail.html', context)
    response.set_cookie(read_key, 'true')
    return response
