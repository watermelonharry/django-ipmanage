# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from models import *
from serializers import *


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
	if request.user.is_authenticated():
		return render(request,
	                  'ipcset_hello.html',
	                  {'firstTitle': u'码流参数批量设置工具',
	                   'firstTitle_content': u'批量设置设备的各项参数',
	                   })


@login_required
def show_basic_info(request):
    return render(request, 'ipcset_basic.html', {'firstTitle': u'码流参数批量设置工具',
                                                    'firstTitle_content': u'批量设置指定IPC的码流参数，同步OSD显示'})

@login_required
def show_basic_model_info(request):
    model_list = BaseTypeTable.objects.all()
    return render_to_response('ipcset_basic_model.html',{'firstTitle': u'码流参数批量设置工具',
                                                    'firstTitle_content': u'设备型号信息查看',
                                                         'model_list':model_list},
                              context_instance=RequestContext(request))

@login_required
def show_settings_info(request):
    setting_list = VideoSettingTable.objects.all()
    return render_to_response('ipcset_settings_table.html', {'firstTitle': u'码流参数批量设置工具',
                                                             'firstTitle_content': u'查看详细参数设置',
                                                             'setting_list': setting_list},
                              context_instance=RequestContext(request))

@login_required
def show_mission_info(request):
    mission_list = MissionInfoTable.objects.all()
    return render_to_response('ipcset_mission_info.html', {'firstTitle': u'码流参数批量设置工具',
                                                           'firstTitle_content': u'查看任务状态',
                                                           'mission_list': mission_list},
                              context_instance=RequestContext(request))

@login_required
def show_mission_detail_info(request, mid):
    detail_list = MissionDetailTable.objects.filter(mission_id=mid)
    return render_to_response('ipcset_mission_detail.html', {'firstTitle': u'码流参数批量设置工具',
                                                             'firstTitle_content': u'查看任务明细',
                                                             'detail_list': detail_list,
                                                             'mission_id': mid},
                              context_instance=RequestContext(request))


"""
apis
"""

@csrf_exempt
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
        data = json.loads(request.body)
        type_obj = BaseTypeTable.objects.get(id=data['type_id'])
        # json_data = BaseTypeSerializer(type_obj).data
        data['type_id'] = type_obj
        data['id'] = None
        data['mac_addr'] = data['mac_addr'].replace('-', '', 4)
        new_setting = VideoSettingTable(**data)
        new_setting.save()
        return JSONResponse({'success': 0}, status=201)

@csrf_exempt
def api_edit_single_videosetting(request, id):
    '''
    显示、更新、删除一个设备设置
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
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        setting.delete()
        return HttpResponse(status=204)


def api_get_model_type(request):
    if request.method == 'GET':
        id_list = map(int, request.GET.getlist('id'))
        if len(id_list) != 0:
            model_list = BaseTypeTable.objects.filter(id__in=id_list)
        else:
            model_list = BaseTypeTable.objects.all()
        serializer = BaseTypeSerializer(model_list, many=True)
        return JSONResponse(serializer.data, status=200)

@csrf_exempt
def api_get_add_put_mission(request):

    if request.method == 'GET':
        mid_list = map(int, request.GET.getlist('mission_id'))
        if len(mid_list) != 0:
            mission_list = MissionInfoTable.objects.filter(mission_id__in=mid_list)
        else:
            mission_list = MissionInfoTable.objects.all()
        serializer = MissionInfoSerializer(mission_list, many=True)
        return JSONResponse(serializer.data, status=200)

    data = JSONParser().parse(request)
    if request.method == 'POST':
        serializer = MissionInfoSerializer(data=data)
        mission_id = data.get('mission_id')
        if serializer.is_valid():
            serializer.save()

            video_id = data.get('detail_id', [])
            setting_set = VideoSettingTable.objects.filter(id__in=video_id)
            for single_setting in setting_set:
                detail = MissionDetailTable(mission_id=mission_id,
                                            mac_addr=single_setting.mac_addr,
                                            current_ip=single_setting.current_ip,
                                            type_id=single_setting.type_id,
                                            set_resolution=single_setting.set_resolution,
                                            set_bitrate=single_setting.set_bitrate,
                                            set_framerate=single_setting.set_framerate,
                                            set_min_resolution=single_setting.set_min_resolution,
                                            set_min_bitrate=single_setting.set_min_bitrate,
                                            set_min_framerate=single_setting.set_min_framerate,
                                            operate_type=single_setting.operate_type)
                detail.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        mid = data.get('mission_id')
        try:
            mission_info = MissionInfoTable.objects.get(mission_id=mid)
            mission_info.delete()
            mission_detail_list = MissionDetailTable.objects.filter(mission_id=mid)
            for detail in mission_detail_list:
                detail.delete()
            return JSONResponse({'delete':'success'}, status=200)
        except:
            return JSONResponse({'delete':'error'}, status=400)


    if request.method == 'PUT':
        mid = data.get('mission_id')
        minfo = MissionInfoTable.objects.get(mission_id=mid)
        serializer = MissionInfoSerializer(minfo, data=data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=200)
    return JSONResponse(serializer.errors, status=400)


def api_get_waiting_mission(request):
    if request.method == 'GET':
        try:
            wait_plan_info = MissionInfoTable.objects.filter(progress=0)[0]
            serializer = MissionInfoSerializer(wait_plan_info)
            return JSONResponse(serializer.data)
        except:
            serializer = MissionInfoSerializer()
            return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def api_get_add_put_mission_detail(request, mid):
    """
    任务的详细条目，每个IP的状态
    :param request:
    :return:
    """
    if request.method == 'DELETE':
        try:
            mission_info = MissionInfoTable.objects.get(mission_id=mid)
            mission_info.delete()
            mission_detail_list = MissionDetailTable.objects.filter(mission_id=mid)
            for detail in mission_detail_list:
                detail.delete()
            return JSONResponse({'delete':'success'}, status=200)
        except:
            return JSONResponse({'delete':'error'}, status=400)

    if request.method == 'GET':
        all_detail_info = MissionDetailTable.objects.filter(mission_id=mid)
        if type(all_detail_info) is QuerySet:
            serializer = MissionDetailSerializer(all_detail_info, many=True)
        else:
            serializer = MissionDetailSerializer(all_detail_info)
        return JSONResponse(serializer.data)

    data = JSONParser().parse(request)
    if request.method == 'POST':
        # todo:将记录添加至数据库
        serializer = MissionDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    if request.method == 'PUT':
        # todo:修改指定记录的状态
        id = data.get('id')
        mission_detail = MissionDetailTable.objects.get(id=id)
        serializer = MissionDetailSerializer(mission_detail, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def api_add_put_discover_mission_detail(request, mid):
    """
    发现设备任务-添加发现的条目至数据表
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)

        mac_addr=data.get('mac_addr')
        model_name = data.pop('model_name')

        try:
            type_id = BaseTypeTable.objects.get(model_name__contains=model_name)
        except Exception as e:
            ##DoesNotExist 型号不存在
            type_id = BaseTypeTable.objects.get(model_name=u'未知型号')

        if type_id.model_name != u'未知型号':
            #未索引型号不添加至VideoSetting
            try:
                ##查找旧的VideoSetting
                old_setting = VideoSettingTable.objects.get(mac_addr=mac_addr)
                data['status'] = 1
                serializer = VideoSettingSerializer(old_setting, data=data)
                if serializer.is_valid():
                    serializer.save()
            except Exception as e:
                ## add new video setting
                data['status'] = 2
                mission_id = data.pop('mission_id')
                new_setting = VideoSettingTable(type_id=type_id, **data)
                new_setting.save()
                data['mission_id'] = mission_id
        else:
            data['status'] = 6

        try:
            ##增加MissionDetail
            editor_name = data.pop('editor_name')
            detail_obj = MissionDetailTable(type_id=type_id, **data)
            detail_obj.save()
        except Exception as e:
            pass

        return JSONResponse(data, status=201)


def api_get_same_type_by_id(request):
    """
    query the devices which have the same type
    input: {'id':1}
    return: {setting_dict1, setting_dict2...}
    """

    if request.method == 'GET':
        src_id = request.GET.get('id')
        try:
            src_setting = VideoSettingTable.objects.get(id=src_id)
            query_set = VideoSettingTable.objects.filter(type_id=src_setting.type_id).exclude(id=src_id)
            serializer = VideoSettingSerializer(query_set, many=True)
            return JSONResponse(serializer.data, status=200)
        except Exception as e:
            return JSONResponse({'error':e.message}, status=501)

def api_sync_stream_setting(request):
    """
    sync settings from source device to dst device
    input: src device id dict, eg. {'id':1}
    method: POST
    return:
        success:    {'success':'0'}, status_code = 200
        fail:   {'error': error_msg}, status_code = 501
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        src_id = data.get('src_id')
        dst_id_list = data.get('dst_id')
        editor_name = data.get('editor_name')
        try:
            src_setting = VideoSettingTable.objects.get(id=src_id)
            src_dict = VideoSettingPartSerializer(src_setting).data
            src_dict['editor_name']=editor_name
            VideoSettingTable.objects.filter(id__in=dst_id_list).update(**src_dict)
            return JSONResponse({'success': 0}, status=200)
        except Exception as e:
	        return JSONResponse({'error': e.message}, status=501)


def api_batch_detele_videosetting(request):
	"""
	delete videosettings by id list
	input: id list in json dict form, eg. {'id': [1,2,3,4,5]}
	method: POST
	return:
		success   {'success':0},  status_code=204
	    fail {'error': error_msg}, status_code=501
	"""
	if request.method == 'POST':
		data = JSONParser().parse(request)
		delete_id_list = data.get('id')
		try:
			setting_list = VideoSettingTable.objects.filter(id__in=delete_id_list)
			setting_list.delete()
		except Exception as e:
			return JSONResponse({'error':e.message}, status=501)
