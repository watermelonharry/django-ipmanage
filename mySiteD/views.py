# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from forms import UserFrom


def hello(request):
    replyList =[{'name':u'DNS报文解析测试工具', 'url':'/dnstest/testsuitelist'},
                ]
    firstTitle = u'WELCOME!! :D'
    firstTitle_content = u'这里集成了一些测试会用到的小工具。点击上方工具列表查看。'
    return render(request, 'hello.html', locals())


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method =='POST':
        return render(request, 'login.html')


def time(request):
    firstTitle = u'时间显示'
    firstTitle_content = datetime.datetime.now()
    return render_to_response('current_time.html', {'current_time':firstTitle_content,
                                                    'firstTitle':firstTitle,
                                                    'firstTitle_content':firstTitle_content})

def pre_test(request):
    firstTitle = u'测试页面'
    firstTitle_content = u'按键测试'
    return render_to_response('pre_test.html', locals())

def register(request):
    secondTitle = u'注册用户'
    if request.method == 'POST':
        form = UserFrom(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('register.html', locals())
    else:
        form = UserFrom
    return render_to_response('register.html', locals())