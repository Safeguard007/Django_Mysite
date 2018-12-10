from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import LoginForm, RegisterForm


def index(request):
    return render(request, 'home.html')


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')


def bad_request(request):
    return render(request, '400.html')


@csrf_exempt
def user_login(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = auth.authenticate(request, username=username, password=password)
            # if user is not None:
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
            # else:
            #     login_form.add_error(None, '用户名或密码错误')
    else:
        login_form = LoginForm()

    context = dict()
    context['login_form'] = login_form
    return render(request, 'login.html', context)
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    #
    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'login.html', {'message': '用户名或密码错误'})


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
    return render(request, 'register.html', context)
