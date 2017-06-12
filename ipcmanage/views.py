# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from serializers import CnStaticIpTableSerializer, CnIpcLogDetailSerializer, CnOperateInfoSerializer
from models import CnStaticIpcTable, CnIpcChangeLogDetail, CnIpcOperateInfo
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


TD_LIST = []

"""
views

"""


def welcome(request):
    return render_to_response('ipc_hello.html', {'firstTitle': u'IPC批量IP设置工具',
                                                 'firstTitle_content': u'批量管理IPC的IP地址'})


def show_ip_table(request):
    ip_list = CnStaticIpcTable.objects.all()
    return render_to_response('ipc_mac_ip_table.html', {'firstTitle': u'IPC批量IP设置工具',
                                                        'firstTitle_content': u'批量管理IPC的IP地址',
                                                        'ip_list': ip_list})


def api_start_set_ipc(request):
    """
    接收开始任务的json
    eg.
    """
    if request.method == 'GET':
        all_operate_info = CnIpcOperateInfo.objects.all()
        serializer = CnOperateInfoSerializer(all_operate_info, many=True)
        return JSONResponse(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        op_id = data.get('operate_id')
        #todo:开始任务线程
        serializer = CnOperateInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


def api_operate_info(request, operate_id):
    """
    显示、更新任务信息
    """
    try:
        op_info = CnIpcOperateInfo.objects.get(operate_id=operate_id)
    except CnIpcOperateInfo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CnOperateInfoSerializer(op_info)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CnOperateInfoSerializer(op_info, data=data)

        if data['operate_id'] != operate_id:
            return JSONResponse(serializer.errors, status=400)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)


def api_operate_detail(request):
    """
    任务的详细条目，每个IP的状态
    :param request: 
    :return: 
    """
    data = JSONParser().parse(request)
    if request.method == 'GET':
        operate_id = data.get('operate_id')
        all_detail_info = CnIpcChangeLogDetail.objects.filter(operate_id=operate_id)
        if type(all_detail_info) is QuerySet:
            serializer = CnIpcLogDetailSerializer(all_detail_info, many=True)
        else:
            serializer = CnIpcLogDetailSerializer(all_detail_info)

        return JSONResponse(serializer.data)

        #todo:获取指定op_id对应的log_list
    if request.method == 'POST':
        #todo:将记录添加至数据库
        serializer = CnIpcLogDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


# @csrf_exempt
def api_ip_list(request):
    '''
    展示所有的ip-mac映射，或者创建新的ip-mac映射关系
    '''
    if request.method == 'GET':
        ip_macs = CnStaticIpcTable.objects.all()
        serializer = CnStaticIpTableSerializer(ip_macs, many=True)

        # to json str
        # j=JSONRenderer().render(serializer.data)
        # to dict list
        # import json
        # g = json.loads(j)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CnStaticIpTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


# @csrf_exempt
def api_ip_mac_detail(request, id):
    '''
    显示、更新、删除一个ip-mac
    '''
    try:
        ip_mac = CnStaticIpcTable.objects.get(id=id)
    except CnStaticIpcTable.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CnStaticIpTableSerializer(ip_mac)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CnStaticIpTableSerializer(ip_mac, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        ip_mac.delete()
        return HttpResponse(status=204)
