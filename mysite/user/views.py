from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail

from .models import Profile
from .forms import LoginForm, RegisterForm, ChangeProflieForm, BlindEmailForm

import string
import random


def user_inf(request):
    return render(request, 'user/inf.html')


def user_logout(request):
    auth.logout(request)
    return render(request, 'user/logout.html')


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
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = dict()
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username, password, email)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()

    context = dict()
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)


def change_proflie(request):
    if request.method == 'POST':
        form = ChangeProflieForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangeProflieForm()

    context = dict()
    context['form'] = form
    context['return_back_url'] = request.GET.get('from', reverse('home'))

    return render(request, 'user/change_profile.html', context)


def blind_email(request):
    if request.method == 'POST':
        form = BlindEmailForm(request.POST)
        if form.is_valid():
            pass
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = BlindEmailForm()

    context = dict()
    context['form'] = form
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
