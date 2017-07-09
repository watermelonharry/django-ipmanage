# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
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


"""
views

"""

@login_required
def welcome(request):
    return render_to_response('ipc_hello.html', {'firstTitle': u'IPC批量IP设置工具',
                                                 'firstTitle_content': u'批量管理IPC的IP地址'},
                              context_instance=RequestContext(request))

@login_required
def show_ip_table(request):
    ip_list = CnStaticIpcTable.objects.all()
    return render_to_response('ipc_mac_ip_table.html', {'firstTitle': u'IPC批量IP设置工具',
                                                        'firstTitle_content': u'批量管理IPC的IP地址',
                                                        'ip_list': ip_list},
                              context_instance=RequestContext(request))
@login_required
def show_mission_datail(request, operate_id):
    detail_list = CnIpcChangeLogDetail.objects.filter(operate_id=operate_id)
    return render_to_response('mission_detail_table.html', {'firstTitle': u'IPC批量IP设置工具',
                                                            'firstTitle_content': u'查看任务明细',
                                                            'detail_list': detail_list,
                                                            'operate_id': operate_id},
                              context_instance=RequestContext(request))
@login_required
def show_mission_info(request):
    mission_info_list = CnIpcOperateInfo.objects.all()
    return render_to_response('mission_info.html',{'firstTitle': u'IPC批量IP设置工具',
                                                    'firstTitle_content': u'查看历史任务',
                                                    'info_list': mission_info_list},
                              context_instance=RequestContext(request))
@login_required
def download_iptables(reqeust):
    ip_list = (k.get_content() for k in CnStaticIpcTable.objects.all())
    # ip_list = CnStaticIpTableSerializer(ip_list, many=True).data
    # content_json = unicode(JSONRenderer().render(ip_list))
    response = StreamingHttpResponse(ip_list, content_type = 'APPLICATION/OCTET=STREAM')
    response['Content-Disposition'] = 'attachment; filename=ip_mac.txt'
    # response['Content-Length'] = len(ip_list)
    return response

@csrf_exempt
def api_plan_unfinished(request):
    """
    显示未开始的任务
    """
    if request.method == 'GET':
        try:
            wait_plan_info = CnIpcOperateInfo.objects.filter(progress=0)[0]
            serializer = CnOperateInfoSerializer(wait_plan_info)
            return JSONResponse(serializer.data)
        except:
            serializer = CnOperateInfoSerializer()
            return JSONResponse(serializer.errors, status=400)

@csrf_exempt
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

        # global TD_LIST
        # if len(TD_LIST) == 0:
        #     ip_macs = CnStaticIpcTable.objects.all()
        #     serializer = CnStaticIpTableSerializer(ip_macs, many=True)
        #     j=JSONRenderer().render(serializer.data)
        #     ipcmanager = ipcc.IPCCtrlManager(tid=op_id,
        #                                   scanPlanJsonStr=json.dumps(data),
        #                                   settings=j)
        #     TD_LIST.append(ipcmanager)
        #     ipcmanager.start()

        serializer = CnOperateInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)

        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
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

    elif request.method == 'DELETE':
        op_info.delete()
        return JSONResponse({'delete':'success'}, status=200)

@csrf_exempt
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


@csrf_exempt
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
        data['mac_addr'] = data['mac_addr'].replace('-', '', 4)
        serializer = CnStaticIpTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
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
