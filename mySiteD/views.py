# -*- coding: utf-8 -*-

from django.shortcuts import render

from feedback.forms import FeedBackForm


def hello(request):
    firstTitle = u'WELCOME!! :D'
    firstTitle_content = u'测试工具集合。点击上方工具列表进行查看。'
    return render(request, 'hello.html', {'firstTitle':firstTitle,'firstTitle_content':firstTitle_content})
