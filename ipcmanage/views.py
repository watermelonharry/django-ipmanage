# -*- coding: utf-8 -*-


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *

def welcome(request):
    return render_to_response('ipc_hello.html',{'firstTitle':u'IPC批量IP设置工具',
                                                  'firstTitle_content':u'批量管理IPC的IP地址'})

def show_ip_table(request):
    ip_list = CnStaticIpcTable.objects.all()
    return render_to_response('ipc_mac_ip_table.html',{'firstTitle':u'IPC批量IP设置工具',
                                                       'firstTitle_content':u'批量管理IPC的IP地址',
                                                       'ip_list':ip_list})

from rest_framework import viewsets
from serializers import CnStaticIpTableSerializer
from models import CnStaticIpcTable

# class IpTableViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = CnStaticIpcTable.objects.all()
#     serializer_class = CnStaticIpTableSerializer

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class JSONResponse(HttpResponse):
    '''
    用来返回json数据
    '''
    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse,self).__init__(content,**kwargs)

# @csrf_exempt
def api_ip_list(request):
    '''
    展示所有的ip-mac映射，或者创建新的ip-mac映射关系
    '''
    if request.method == 'GET':
        ip_macs = CnStaticIpcTable.objects.all()
        serializer = CnStaticIpTableSerializer(ip_macs,many=True)

        #json str
        # j=JSONRenderer().render(serializer.data)
        # #dict list
        # import json
        # g = json.loads(j)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CnStaticIpTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data,status=201)
        return JSONResponse(serializer.errors,status=400)

# @csrf_exempt
def api_ip_mac_detail(request,id):
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
        serializer = CnStaticIpTableSerializer(ip_mac,data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors,status=400)

    elif request.method == 'DELETE':
        ip_mac.delete()
        return HttpResponse(status=204)