# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from forms import UserFrom

def hello(request):
    replyList =[{'name':u'DNS报文解析测试工具', 'url':'/dnstest/testsuitelist'},
                ]
    firstTitle = u'WELCOME!! :D'
    secondTitle = u'已有测试工具列表'
    return render_to_response('hello.html', locals())


def time(request):
    now = datetime.datetime.now()
    firstTitle = u'时间显示'
    secondTitle = u'tttttttttttt'
    return render_to_response('current_time.html', {'current_time':now,
                                                    'firstTitle':firstTitle,
                                                    'secondTitle':secondTitle})


def pre_test(request):
    now = datetime.datetime.now()
    firstTitle = u'测试工具'
    secondTitle = u'DNS测试'
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