# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse

@login_required
def show_iot_main_page(request):
    return render_to_response('iot_mainpage.html', {'firstTitle': u'IOT测试',
                                                 'firstTitle_content': u'hhhhh'},
                              context_instance=RequestContext(request))
