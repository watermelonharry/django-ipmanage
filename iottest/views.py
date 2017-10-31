# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse
from models import IotDeviceTable, MissionTable, MissionDetailTable
from serializers import IotDeviceSerializer, MissionTableGetSerializer, MissionDetailGetSerializer, \
    MissionDetailPostSerializer, MissionTablePostSerializer
from userManage.models import ApiKeyModel


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
                                                    'firstTitle_content': u'-兼容性测试管理'},
                              context_instance=RequestContext(request))


@login_required
def show_iot_sut_page(request):
    return render_to_response('iot_sut_page.html', {'firstTitle': u'IOT测试',
                                                    'firstTitle_content': u'-查看陪测设备详细'},
                              context_instance=RequestContext(request))


@login_required
def show_mission_detail(request, m_id):
    detail_list = MissionDetailTable.get_details_by_mission_id(m_id)
    return render_to_response('iot_mission_detail.html', {'firstTitle': u'IOT测试',
                                                          'firstTitle_content': u'-查看任务详细',
                                                          'mission_id': m_id,
                                                          'mission_detail_list': detail_list},
                              context_instance=RequestContext(request))
@login_required
def show_mission_compare(request):
    parser =FormatJsonParser(request)
    src_id = parser.get_content().get("src",[0])[0]
    dst_id = parser.get_content().get("dst",[0])[0]
    return render_to_response('iot_mission_compare.html', {'firstTitle': u'IOT测试',
                                                          'firstTitle_content': u'-分析任务差异',
                                                           'src_id':src_id,
                                                           'dst_id':dst_id},
                              context_instance=RequestContext(request))

@login_required
def download_sut_data(request):
    """down load data in file"""
    sut_list = (sut.get_download_content() for sut in IotDeviceTable.get_sut_list())
    response = StreamingHttpResponse(sut_list, content_type='APPLICATION/OCTET=STREAM')
    response['Content-Disposition'] = 'attachment; filename=iot_device_list.dat'
    return response



@login_required
def show_mission_list(request):
    return render_to_response('iot_mission_list.html', {'firstTitle': u'IOT测试',
                                                        'firstTitle_content': u'-查看历史任务'},
                              context_instance=RequestContext(request))


"""
apis here
"""


# @csrf_exempt
def api_get_add_iot_suts(request):
    if request.method == "GET":
        sut_ids = map(int, FormatJsonParser(request).get_content().get('id', []))
        sut_ids.sort()
        if not sut_ids:
            sut_list = IotDeviceTable.get_sut_list(ordering='ip')
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
def api_out_get_add_iot_suts(request):
    if request.method == "GET":
        parser = FormatJsonParser(request)
        if ApiKeyModel.has_ak(ak=parser.get_ak()):
            sut_ids = map(int, parser.get_content().get('id', []))
            sut_ids.sort()
            if not sut_ids:
                sut_list = IotDeviceTable.get_sut_list()
            else:
                sut_list = IotDeviceTable.objects.filter(id__in=sut_ids)
            serializer = IotDeviceSerializer(sut_list, many=True)
            return SuccessJsonResponse(serializer.data)
        else:
            return ErrorJsonResponse("invalid ak")

    elif request.method == "POST":
        parser = FormatJsonParser(request)
        if ApiKeyModel.has_ak(ak=parser.get_ak()):
            data = parser.get_data()
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
            return ErrorJsonResponse("invalid ak")
    else:
        return ErrorJsonResponse(data="method not supported")



@csrf_exempt
def api_get_iot_sut_ids(request):
    try:
        if request.method == "GET":
            return SuccessJsonResponse(data=IotDeviceTable.get_sut_ids())
        else:
            return ErrorJsonResponse(data="method not supported")
    except Exception as e:
        return ErrorJsonResponse(data="{0}".format(e))


@csrf_exempt
def api_get_add_put_delete_missions(request):
    try:
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
                    return SuccessJsonResponse(data=serializer.data)
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
                    serializer = MissionTablePostSerializer(ori_mission, data=p_content)
                    if serializer.is_valid():
                        serializer.save()
                        return SuccessJsonResponse(data={'success': [m_id],'mission_status':ori_mission.mission_status})
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
                        serializer = MissionTablePostSerializer(ori_mission, data=single_mission)
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
    except Exception as e:
        return ErrorJsonResponse(data="{0}".format(e))


@csrf_exempt
def api_outter_get_add_put_delete_missions(request):
    try:
        if request.method == "GET":
            mission_ids = request.GET.get('id', [])
            if not mission_ids:
                mission_list = MissionTable.objects.all()
            else:
                mission_list = MissionTable.objects.filter(id__in=mission_ids)
            if len(mission_list) == 1:
                serializer = MissionTableGetSerializer(mission_list[0])
            else:
                serializer = MissionTableGetSerializer(mission_list, many=True)
            return SuccessJsonResponse(serializer.data)

        elif request.method == "POST":
            parser = FormatJsonParser(request)
            if ApiKeyModel.has_ak(ak=parser.get_ak()):
                m_data = parser.get_data()
                if m_data:
                    serializer = MissionTablePostSerializer(data=m_data)
                    if serializer.is_valid():
                        serializer.save()
                        return SuccessJsonResponse(data=serializer.data)
                    else:
                        return ErrorJsonResponse(data=serializer.errors)
                else:
                    return ErrorJsonResponse(data="post data is empty")
            else:
                return ErrorJsonResponse(data="invalid ak")

        elif request.method == "PUT":
            parser = FormatJsonParser(request)
            if ApiKeyModel.has_ak(ak=parser.get_ak()):
                p_content = parser.get_data()

                if isinstance(p_content, dict):
                    m_id = p_content.get('id')
                    try:
                        ori_mission = MissionTable.objects.get(id=m_id)
                        serializer = MissionTablePostSerializer(ori_mission, data=p_content)
                        if serializer.is_valid():
                            serializer.save()
                            return SuccessJsonResponse(data={'success': [m_id],'mission_status':ori_mission.mission_status})
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
                            serializer = MissionTablePostSerializer(ori_mission, data=single_mission)
                            if serializer.is_valid():
                                serializer.save()
                                success_ids.append(m_id)
                            else:
                                error_ids.append({m_id: serializer.errors})
                        except Exception as e:
                            error_ids.append({m_id: '{0}'.format(e)})
                    return SuccessJsonResponse(data={"success": success_ids, "errors": error_ids})
            else:
                return ErrorJsonResponse(data="invalid ak")

        elif request.method == 'DELETE':
            p_data = FormatJsonParser(request)
            if ApiKeyModel.has_ak(ak=p_data.get_ak()):
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
                return ErrorJsonResponse(data="invalid ak")
        else:
            return ErrorJsonResponse(data="unsupported method")
    except Exception as e:
        return ErrorJsonResponse(data="{0}".format(e))


@csrf_exempt
def api_get_mission_progress(request, m_id):
    try:
        if request.method == "GET":
            mission = MissionTable.objects.get(id=m_id)
            ret_data = {"mission_status": mission.mission_status,
                        "mission_progress": mission.mission_progress,
                        "mission_total": mission.mission_total}
            return SuccessJsonResponse(data=ret_data)
        else:
            return ErrorJsonResponse(data="unsupported method")
    except Exception as e:
        return ErrorJsonResponse(data="{0}".format(e))


@csrf_exempt
def api_out_get_mission_progress(request, m_id):
    try:
        post_data = FormatJsonParser(request)
        if ApiKeyModel.has_ak(ak=post_data.get_ak()):
            if request.method == "GET":
                mission = MissionTable.objects.get(id=m_id)
                ret_data = {"mission_status": mission.mission_status,
                            "mission_progress": mission.mission_progress,
                            "mission_total": mission.mission_total}
                return SuccessJsonResponse(data=ret_data)
            else:
                return ErrorJsonResponse(data="unsupported method")
        return ErrorJsonResponse(data="invalid ak")
    except Exception as e:
        return ErrorJsonResponse(data="{0}".format(e))

@csrf_exempt
def api_get_add_mission_details(request, m_id):
    if request.method == "GET" and m_id:
        m_details = MissionDetailTable.get_details_by_mission_id(m_id)
        serializer = MissionDetailGetSerializer(m_details, many=True)
        return SuccessJsonResponse(data=serializer.data)

    elif request.method == "POST":
        post_data = FormatJsonParser(request)
        serializer = MissionDetailPostSerializer(data=post_data.get_data())
        if serializer.is_valid():
            serializer.save()
            return SuccessJsonResponse(data=serializer.data)
        else:
            return ErrorJsonResponse(data=serializer.errors)

    else:
        return ErrorJsonResponse(data="{0} is not supported".format(request.method))


@csrf_exempt
def api_outter_get_add_mission_details(request, m_id):
    if request.method == "GET" and m_id:
        m_details = MissionDetailTable.get_details_by_mission_id(m_id)
        serializer = MissionDetailGetSerializer(m_details, many=True)
        return SuccessJsonResponse(data=serializer.data)

    elif request.method == "POST":
        post_data = FormatJsonParser(request)
        if ApiKeyModel.has_ak(ak=post_data.get_ak()):
            serializer = MissionDetailPostSerializer(data=post_data.get_data())
            if serializer.is_valid():
                serializer.save()
                return SuccessJsonResponse(data=serializer.data)
            else:
                return ErrorJsonResponse(data=serializer.errors)
        else:
            return ErrorJsonResponse(data='invalid ak')
    else:
        return ErrorJsonResponse(data="{0} is not supported".format(request.method))

@csrf_exempt
def api_inner_compare_two_mission(request):
	"""
	比较两个任务的明细。
	接受GET方法。
	:param request:
	:return: list(CompareResult)
	"""
	if request.method == "GET":
		parse_content = FormatJsonParser(request).get_content()
		src_id= parse_content.get("src_id",None).pop()
		dst_id=parse_content.get("dst_id",None).pop()
		if src_id and dst_id:
			try:
				src_detail_list = MissionDetailTable.get_details_by_mission_id(m_id=src_id)
				dst_detail_list = MissionDetailTable.get_details_by_mission_id(m_id=dst_id)
				result_list = MissionDetailTable.compare_multi_details(src=src_detail_list,dst=dst_detail_list)
				return SuccessJsonResponse(data=result_list)
			except Exception as e:
				return ErrorJsonResponse("{0}".format(e))
		else:
			return ErrorJsonResponse("need src_id and dst_id")

	else:
		return ErrorJsonResponse("{0} is not supported".format(request.method))