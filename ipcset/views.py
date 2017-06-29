# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render_to_response
from serializers import *
from models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json


class JSONResponse(HttpResponse):
    '''
    用来返回json数据
    '''

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


"""
views

"""


def welcome(request):
    return render_to_response('ipcset_hello.html', {'firstTitle': u'码流参数批量设置工具',
                                                 'firstTitle_content': u'批量设置指定IPC的码流参数，同步OSD显示'})

def show_basic_info(request):

    return render_to_response('ipcset_basic.html', {'firstTitle': u'码流参数批量设置工具',
                                                        'firstTitle_content': u'批量设置指定IPC的码流参数，同步OSD显示'})

def show_settings_info(request):
    setting_list = VideoSettingTable.objects.all()
    return render_to_response('ipcset_settings_table.html',{'firstTitle': u'码流参数批量设置工具',
                                                    'firstTitle_content': u'查看详细参数设置',
                                                    'setting_list': setting_list})

"""
apis
"""


# @csrf_exempt
def api_add_or_get_videosetting(request):
    '''
    '''
    if request.method == 'GET':
        id_list = map(int, request.GET.getlist('id'))
        if len(id_list) != 0:
            model_list = VideoSettingTable.objects.filter(id__in=id_list)
        else:
            return JSONResponse(VideoSettingSerializer().errors, status=400)
        serializer = VideoSettingSerializer(model_list, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['mac_addr'] = data['mac_addr'].replace('-', '', 4)
        serializer = VideoSettingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


# @csrf_exempt
def api_edit_single_videosetting(request, id):
    '''
    显示、更新、删除一个ip-mac
    '''
    try:
        setting = VideoSettingTable.objects.get(id=id)
    except VideoSettingTable.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VideoSettingSerializer(setting)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VideoSettingSerializer(setting, data=data)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data,status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        setting.delete()
        return HttpResponse(status=204)

def api_get_model_type(request):
    if request.method == 'GET':
        id_list =map(int,request.GET.getlist('id'))
        if len(id_list) != 0:
            model_list = BaseTypeTable.objects.filter(id__in=id_list)
        else:
            model_list = BaseTypeTable.objects.all()
        serializer = BaseTypeSerializer(model_list, many=True)
        return JSONResponse(serializer.data, status=200)

def api_get_add_mission(request):
    if request.method == 'GET':
        mid_list =map(int,request.GET.getlist('mission_id'))
        if len(mid_list) != 0:
            model_list = MissionInfoTable.objects.filter(mission_id__in=mid_list)
        else:
            model_list = MissionInfoTable.objects.all()
        serializer = MissionDetailSerializer(model_list, many=True)
        return JSONResponse(serializer.data, status=200)

    data = JSONParser().parse(request)
    if request.method == 'POST':
        serializer = MissionInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    if request.method == 'PUT':
        mid = request.PUT.get('mission_id')
        minfo = MissionInfoTable.objects.get(mission_id=mid)
        serializer = MissionInfoSerializer(minfo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)


def api_get_add_put_mission_detail(request, mid):
    """
    任务的详细条目，每个IP的状态
    :param request:
    :return:
    """
    data = JSONParser().parse(request)
    if request.method == 'GET':
        all_detail_info = MissionDetailTable.objects.filter(mission_id=mid)
        if type(all_detail_info) is QuerySet:
            serializer = MissionDetailSerializer(all_detail_info, many=True)
        else:
            serializer = MissionDetailSerializer(all_detail_info)
        return JSONResponse(serializer.data)

    if request.method == 'POST':
        # todo:将记录添加至数据库
        serializer = MissionDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    if request.method == 'PUT':
        # todo:修改指定记录的状态
        id =  data.get('id')
        mission_detail = MissionDetailTable.objects.get(id=id)
        serializer = MissionDetailSerializer(mission_detail, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

