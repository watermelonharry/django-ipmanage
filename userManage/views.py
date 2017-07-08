# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import RequestContext


# Create your views here.


def user_login(request):

	if request.method == 'GET':
		return render(request, 'user_login.html', {'notice':u'欢迎登陆'})

	if request.method == 'POST':
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		verified_user = authenticate(username= user_name, password=password)

		if verified_user is not None:
			if verified_user.is_active:
				return render(request, 'user_success.html', {'notice': u'登陆成功！即将跳转...', 'next_url':'/hello/'})
			else:
				pass
		else:
			return render(request, 'user_login.html', {'notice':u'请输入正确的用户名密码'})


def user_register(request):
    if request.method == 'GET':
        return render(request, 'user_register.html', {'notice':u'新用户注册'})

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        email_addr = request.POST.get('inputEmail')
        real_name = request.POST.get('real_name')

        try:
            new_user = User.objects.create_user(username=user_name,
                                                password=password,
                                                email=email_addr,
                                                first_name=real_name)
            new_user.is_staff = True
            new_user.save()
            return render(request,'user_login.html', {'notice':u'注册成功！请登录'})
        except Exception as e:
            if 'username is not unique' in e.message:
                return  render(request, 'user_register.html', {'notice':u'注册失败:用户名已存在'})