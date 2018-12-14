from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from .models import Profile
from .forms import LoginForm, RegisterForm, ChangeProflieForm, BlindEmailForm

import string
import random


def user_inf(request):
    if not (request.user.is_authenticated):
        return render(request, 'home.html')
    return render(request, 'user/inf.html')


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def login_modal(request):
    login_form = LoginForm(request.POST)
    data = dict()
    if login_form.is_valid():
        user = user_login.clean_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


@csrf_exempt
def user_login(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return HttpResponseRedirect(request.session['login_from'])
    else:
        login_form = LoginForm()
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')

    context = dict()
    context['form'] = login_form
    context['form_head'] = '登录'
    return render(request, 'user/login.html', context)


@csrf_exempt
def user_register(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username, password=password, email=email)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect(request.session['register_from'])
    else:
        register_form = RegisterForm()
        request.session['register_from'] = request.META.get('HTTP_REFERER', '/')

    context = dict()
    context['form'] = register_form
    context['form_head'] = '注册'
    return render(request, 'user/register.html', context)


def change_proflie(request):
    if request.method == 'POST':
        form = ChangeProflieForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return HttpResponseRedirect(request.session['change_profile_from'])
    else:
        form = ChangeProflieForm()
        request.session['change_profile_from'] = request.META.get('HTTP_REFERER', '/')

    context = dict()
    context['form'] = form
    context['form_head'] = '更改个人信息'
    context['return_back_url'] = request.GET.get('from', reverse('home'))

    return render(request, 'user/change_profile.html', context)


def blind_email(request):
    if request.method == 'POST':
        form = BlindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return HttpResponseRedirect(request.session['blind_email_from'])
    else:
        form = BlindEmailForm()
        request.session['blind_email_from'] = request.META.get('HTTP_REFERER', '/')

    context = dict()
    context['form'] = form
    context['form_head'] = '绑定Email'
    context['return_back_url'] = request.GET.get('from', reverse('home'))

    return render(request, 'user/blind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = dict()
    if email != '':
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['blind_email_code'] = code

        send_mail(
            '绑定邮箱操作',
            '验证码：%s' % code,
            'safeguard@163.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'

    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)
