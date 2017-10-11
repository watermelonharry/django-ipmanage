# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse
from models import IotDeviceTable, MissionTable, MissionDetailTable
from serializers import IotDeviceSerializer


@login_required
def show_iot_main_page(request):
    return render_to_response('iot_mainpage.html', {'firstTitle': u'IOT测试',
                                                    'firstTitle_content': u'hhhhh'},
                              context_instance=RequestContext(request))


@login_required
def show_iot_sut_page(request):
    return render_to_response('iot_sut_page.html', {'firstTitle': u'IOT测试',
                                                    'firstTitle_content': u'-查看陪测设备详细'},
                              context_instance=RequestContext(request))


"""
apis here
"""


def api_iot_sut_page(request):
    if request.method == "GET":
        sut_list = IotDeviceTable.objects.all()
        serializer = IotDeviceSerializer(sut_list, many=True)
        return SuccessJsonResponse(serializer.data)
    else:
        return ErrorJsonResponse(data="method not supported")
