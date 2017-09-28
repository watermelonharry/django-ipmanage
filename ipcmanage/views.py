# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from serializers import IpMacTableSerializer, IpMissionDetailSerializer, IpMissionSerializer
from models import StaticIpMacTable, IpMissionDetailTable, IpMissionTable
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse


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
    return render_to_response('ipc_hello.html', {'firstTitle': u'批量IP设置',
                                                 'firstTitle_content': u'将设备恢复到出厂设置，随后将其设置到指定IP'},
                              context_instance=RequestContext(request))


@login_required
def show_ip_table(request):
    ip_list = StaticIpMacTable.objects.all()
    return render_to_response('ipc_mac_ip_table.html',
                              {'firstTitle': u'IP批量设置',
                               'firstTitle_content': u'开始设置后，系统会自动连接指定IP，查找其对应的IP，随后对设备进行“恢复出厂-设置至指定IP-更新OSD”的操作',
                               'ip_list': ip_list},
                              context_instance=RequestContext(request))


@login_required
def show_mission_datail(request, operate_id):
    detail_list = CnIpcChangeLogDetail.objects.filter(operate_id=operate_id)
    create_time = IpMissionTable.objects.get(operate_id=operate_id).create_time
    return render_to_response('mission_detail_table.html', {'firstTitle': u'IP批量设置',
                                                            'firstTitle_content': u'查看任务明细',
                                                            'detail_list': detail_list,
                                                            'create_time': create_time},
                              context_instance=RequestContext(request))


@login_required
def show_mission_info(request):
    mission_info_list = IpMissionTable.objects.all()
    return render_to_response('mission_info.html', {'firstTitle': u'IP批量设置',
                                                    'firstTitle_content': u'查看任务信息',
                                                    'info_list': mission_info_list},
                              context_instance=RequestContext(request))


@login_required
def download_iptables(reqeust):
    ip_list = (k.get_content() for k in StaticIpMacTable.objects.all())
    response = StreamingHttpResponse(ip_list, content_type='APPLICATION/OCTET=STREAM')
    response['Content-Disposition'] = 'attachment; filename=ip_mac.dat'
    return response


@csrf_exempt
def api_plan_unfinished(request):
    """
    显示未开始的任务
    method: get
    return:
        success: {json_data}
        failed: {'error':1}
    """
    if request.method == 'GET':
        try:
            wait_plan_info = IpMissionTable.objects.filter(progress=0)[0]
            serializer = IpMissionSerializer(wait_plan_info)
            return JSONResponse(serializer.data, status=200)
        except:
            return JSONResponse({'error': 1}, status=400)


@csrf_exempt
def api_start_set_ipc(request):
    """
    接收开始任务的json
    eg.
    """
    if request.method == 'GET':
        all_operate_info = IpMissionTable.objects.all()
        serializer = IpMissionSerializer(all_operate_info, many=True)
        return JSONResponse(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IpMissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)

        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def api_put_get_delete_mission_info(request, operate_id):
    """
    显示、更新任务信息
    """
    try:
        op_info = IpMissionTable.get_mission_by_mission_id(mid=operate_id)
    except Exception as e:
        return ErrorJsonResponse(data="{0}".format(e),status=400)

    if request.method == 'GET':
        serializer = IpMissionSerializer(op_info)
        return SuccessJsonResponse(data=serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IpMissionSerializer(op_info, data=data)

        if data['operate_id'] != operate_id:
            return ErrorJsonResponse(data="mission id not match")

        if serializer.is_valid():
            serializer.save()
            return SuccessJsonResponse(data=serializer.data, status=200)
        return ErrorJsonResponse(data=serializer.errors, status=400)

    elif request.method == 'DELETE':
        op_info.delete()
        return SuccessJsonResponse(data='delete success', status=200)


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
            serializer = IpMissionDetailSerializer(all_detail_info, many=True)
        else:
            serializer = IpMissionDetailSerializer(all_detail_info)

        return JSONResponse(serializer.data)

    # todo:获取指定op_id对应的log_list
    if request.method == 'POST':
        # todo:将记录添加至数据库
        serializer = IpMissionDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def api_get_add_put_ip_mac_table(request):
    '''
    展示所有的ip-mac映射，或者创建新的ip-mac映射关系
    '''
    if request.method == 'GET':
        ip_macs = StaticIpMacTable.objects.all()
        serializer = IpMacTableSerializer(ip_macs, many=True)

        # to json str
        # j=JSONRenderer().render(serializer.data)
        # to dict list
        # import json
        # g = json.loads(j)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if isinstance(data, dict):
            data['mac_addr'] = data['mac_addr'].replace('-', '', 4)
            serializer = IpMacTableSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
        elif isinstance(data, list):
            for record in data:
                record['mac_addr'] = record['mac_addr'].replace('-', '', 4)
                serializer = IpMacTableSerializer(data=record)
                if serializer.is_valid():
                    serializer.save()


@csrf_exempt
def api_get_put_single_mac(request, id):
    '''
    显示、更新、删除一个ip-mac
    '''
    try:
        ip_mac = StaticIpMacTable.objects.get(id=id)
    except StaticIpMacTable.DoesNotExist:
        return ErrorJsonResponse(data="{0} not exist".format(id), status=400)

    if request.method == 'GET':
        serializer = IpMacTableSerializer(ip_mac)
        return SuccessJsonResponse(data=serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IpMacTableSerializer(ip_mac, data=data)
        if serializer.is_valid():
            serializer.save()
            return SuccessJsonResponse(data=serializer.data, status=200)
        else:
            return ErrorJsonResponse(data=serializer.errors, status=400)

    elif request.method == 'DELETE':
        ip_mac.delete()
        return HttpResponse(status=204)
