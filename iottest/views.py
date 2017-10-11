# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse
from models import IotDeviceTable, MissionTable, MissionDetailTable
from serializers import IotDeviceSerializer, MissionTableSerializer, MissionDetailSerializer


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


@login_required
def show_mission_list(request):
    return render_to_response('iot_mission_list.html', {'firstTitle': u'IOT测试',
                                                        'firstTitle_content': u'-查看历史任务'},
                              context_instance=RequestContext(request))


"""
apis here
"""


def api_get_iot_sut_list(request):
    if request.method == "GET":
        sut_ids = request.GET.get('id', [])
        if not sut_ids:
            sut_list = IotDeviceTable.objects.all()
        else:
            sut_list = IotDeviceTable.objects.filter(id__in=sut_ids)
        serializer = IotDeviceSerializer(sut_list, many=True)
        return SuccessJsonResponse(serializer.data)
    else:
        return ErrorJsonResponse(data="method not supported")


def api_get_mission_list(request):
    if request.method == "GET":
        mission_ids = request.GET.get('id', [])
        if not mission_ids:
            mission_list = MissionTable.objects.all()
        else:
            mission_list = MissionTable.objects.filter(id__in=mission_ids)

        serializer = MissionTableSerializer(mission_list, many=True)
        return SuccessJsonResponse(serializer.data)
    else:
        return ErrorJsonResponse(data="method not supported")
