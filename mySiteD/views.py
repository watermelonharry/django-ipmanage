# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext


from feedback.forms import FeedBackForm


def hello(request):
    firstTitle = u'WELCOME!! :D'
    firstTitle_content = u'测试工具管理平台。'
    return render(request, 'hello.html', {'firstTitle':firstTitle,'firstTitle_content':firstTitle_content})

@login_required
def show_instance_tool(request):
    return render_to_response('instant_tools.html', {'firstTitle': u'即时工具',
                                                          'firstTitle_content': u'快速设置，无需等待。只管下发，不管结果。'},
                              context_instance=RequestContext(request))

def show_about_page(request):
    return render_to_response('about.html', {'firstTitle': u'关于本站',
                                                          'firstTitle_content': u'----------'},
                              context_instance=RequestContext(request))
