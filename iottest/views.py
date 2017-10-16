# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse
from models import IotDeviceTable, MissionTable, MissionDetailTable
from serializers import IotDeviceSerializer, MissionTableGetSerializer, MissionDetailSerializer,MissionTablePostSerializer


@csrf_exempt
def api_test_receive_url(request):
    k = request
    formatter = FormatJsonParser(request)
    content = formatter.get_content()
    print("receive {0} data, type {1}, content {2}".format(request.method, type(content), content))
    return SuccessJsonResponse(data=content)


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


@login_required
def show_mission_detail(request):
    return render_to_response('iot_mission_list.html', {'firstTitle': u'IOT测试',
                                                        'firstTitle_content': u'-查看历史任务'},
                              context_instance=RequestContext(request))


"""
apis here
"""


@csrf_exempt
def api_get_add_iot_suts(request):
    if request.method == "GET":
        sut_ids = request.GET.get('id', [])
        if not sut_ids:
            sut_list = IotDeviceTable.objects.all()
        else:
            sut_list = IotDeviceTable.objects.filter(id__in=sut_ids)
        serializer = IotDeviceSerializer(sut_list, many=True)
        return SuccessJsonResponse(serializer.data)

    elif request.method == "POST":
        data = FormatJsonParser(request).get_data()
        if isinstance(data, list):
            serializer = IotDeviceSerializer(data=data, many=True)
        elif isinstance(data, dict):
            serializer = IotDeviceSerializer(data=data)
        else:
            return ErrorJsonResponse(data="worng format")

        if serializer.is_valid():
            serializer.save()
            return SuccessJsonResponse(data=serializer.data)
        else:
            return ErrorJsonResponse(data=serializer.errors)

    else:
        return ErrorJsonResponse(data="method not supported")


@csrf_exempt
def api_get_add_put_delete_missions(request):
    if request.method == "GET":
        mission_ids = request.GET.get('id', [])
        if not mission_ids:
            mission_list = MissionTable.objects.all()
        else:
            mission_list = MissionTable.objects.filter(id__in=mission_ids)

        serializer = MissionTableGetSerializer(mission_list, many=True)
        return SuccessJsonResponse(serializer.data)

    elif request.method == "POST":
        m_data = FormatJsonParser(request).get_data()
        if m_data:
            serializer = MissionTablePostSerializer(data=m_data)
            if serializer.is_valid():
                serializer.save()
                return SuccessJsonResponse(data=m_data)
            else:
                return ErrorJsonResponse(data=serializer.errors)
        else:
            return ErrorJsonResponse(data="post data is empty")
    elif request.method == "PUT":
        p_data = FormatJsonParser(request)
        p_content = p_data.get_data()
        if isinstance(p_content, dict):
            m_id = p_content.get('id')
            try:
                ori_mission = MissionTable.objects.get(id=m_id)
                serializer = MissionTableGetSerializer(ori_mission, data=p_content)
                if serializer.is_valid():
                    serializer.save()
                    return SuccessJsonResponse(data={'success': [m_id]})
                else:
                    return ErrorJsonResponse(data=serializer.errors)
            except Exception as e:
                return ErrorJsonResponse(data="{0}".format(e))
        elif isinstance(p_content, list):
            success_ids = []
            error_ids = []
            for single_mission in p_content:
                m_id = single_mission.get('id')
                try:
                    ori_mission = MissionTable.objects.get(id=m_id)
                    serializer = MissionTableGetSerializer(ori_mission, data=single_mission)
                    if serializer.is_valid():
                        serializer.save()
                        success_ids.append(m_id)
                    else:
                        error_ids.append({m_id: serializer.errors})
                except Exception as e:
                    error_ids.append({m_id: '{0}'.format(e)})
            return SuccessJsonResponse(data={"success": success_ids, "errors": error_ids})

    elif request.method == 'DELETE':
        p_data = FormatJsonParser(request)
        p_content = p_data.get_data()
        if isinstance(p_content, dict):
            m_id = p_content.get('id', [])
            if isinstance(m_id, int):
                m_id = [m_id]
            try:
                MissionTable.objects.get(id__in=m_id).delete()
                return SuccessJsonResponse(data=m_id)
            except Exception as e:
                return ErrorJsonResponse(data="{0}".format(e))
        else:
            return ErrorJsonResponse(data="unsupported data format")

    else:
        return ErrorJsonResponse(data="unsupported method")


@csrf_exempt
def api_get_add_mission_details(request, m_id):
    if request.method == "GET" and m_id:
        m_details = MissionDetailTable.get_details_by_mission_id(m_id)
        serializer = MissionDetailSerializer(m_details, many=True)
        return SuccessJsonResponse(data=serializer.data)

    elif request.method == "POST":
        post_data = FormatJsonParser(request)
        serializer = MissionDetailSerializer(data=post_data.get_data())
        if serializer.is_valid():
            serializer.save()
            return SuccessJsonResponse(data=serializer.data)
        else:
            return ErrorJsonResponse(data=serializer.errors)

    else:
        return ErrorJsonResponse(data="{0} is not supported".format(request.method))
