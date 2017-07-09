# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import RequestContext
import datetime
from forms import UserFrom


def hello(request):
    firstTitle = u'WELCOME!! :D'
    firstTitle_content = u'这里集成了一些测试会用到的小工具。点击上方工具列表查看。'
    return render(request, 'hello.html', {'firstTitle':firstTitle,'firstTitle_content':firstTitle_content})
