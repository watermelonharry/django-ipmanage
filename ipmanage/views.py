# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from serializers import *
from models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from basepkg.jsonreformat import FormatJsonParser, SuccessJsonResponse, ErrorJsonResponse
from django.db import transaction

from userManage.models import ApiKeyModel

"""
views

"""


@login_required
def web_welcome(request):
    """
    显示MAC-IP绑定主页面
    """
    return render_to_response('ipmanage_hello.html', {'firstTitle': u'MAC-IP绑定及恢复[new]',
                                                      'firstTitle_content': u'将设备恢复到出厂设置，随后将其设置到指定IP'},
                              context_instance=RequestContext(request))


@login_required
def web_config_page(request):
    """
    显示配置简表页面
    """
    with transaction.atomic():
        config_list = ConfigTable.objects.all()
    return render_to_response('ipmanage_config_page.html',
                              {'firstTitle': u'MAC-IP绑定及恢复[new]',
                               'firstTitle_content': u'绑定配置管理',
                               'config_list': config_list},
                              context_instance=RequestContext(request))


@login_required
def web_config_detail_page(request, id):
    """
    显示配置明细
    :param request:
    :param id: config_id
    :return: web page
    """
    config = ConfigTable.get_config_by_id(id=id)
    return render_to_response('ipmanage_config_detail_page.html',
                              {'firstTitle': u'MAC-IP绑定及恢复[new]',
                               'firstTitle_content': u'配置管理',
                               'config': config},
                              context_instance=RequestContext(request))


@login_required
def api_get_add_edit_delete_config_list(request):
    """
    配置表列表-api
    :param request: {ak="xxxxx", offset=0,limit=10, params={},}
    """
    if request.method == "GET":
        parser = FormatJsonParser(request)
        # if ApiKeyModel.has_ak(ak=parser.get_ak()):
        try:
            offset = parser.offset
            limit = parser.limit
            id = parser.id

            if id:
                config_list = ConfigTable.objects.get(id=id)
                serializers = ConfigGetterSerializer(config_list)
            else:
                config_list = ConfigTable.objects.all()[offset:limit + offset]
                serializers = ConfigGetterSerializer(config_list, many=True)

            return SuccessJsonResponse(data=serializers.data)
        except Exception as e:
            return ErrorJsonResponse(data=u"{0}".format(e))

    if request.method == "POST":
        try:
            with transaction.atomic():
                parser = FormatJsonParser(request)
                data = parser.get_body_content()
                if isinstance(data, dict):
                    serializer = ConfigPostSerializer(data=data)

                    if serializer.is_valid():
                        serializer.save()
                        return SuccessJsonResponse(data=serializer.data)
                    else:
                        return ErrorJsonResponse(data=serializer.errors)

                else:
                    raise AttributeError("invalid data type")
        except Exception as e:
            return ErrorJsonResponse("{0}".format(e))

    if request.method == "PUT":
        try:
            parser = FormatJsonParser(request)
            data = parser.get_body_content()
            config_id = data.get('id')
            # edit data
            with transaction.atomic():
                ori_config = ConfigTable.get_config_by_id(id=config_id)
                serializer = ConfigPutSerializer(ori_config, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return SuccessJsonResponse(data=serializer.data)
                else:
                    return ErrorJsonResponse(data=serializer.errors)
        except Exception as e:
            return ErrorJsonResponse(data="{0}".format(e))

    if request.method == "DELETE":
        try:
            parser = FormatJsonParser(request)
            id = parser.id
            with transaction.atomic():
                ConfigTable.get_config_by_id(id=id).delete()
                return SuccessJsonResponse({"id":id})
        except Exception as e:
            return ErrorJsonResponse(data="{0}".format(e))

    else:
        return ErrorJsonResponse("unsupported http method")


@login_required
def api_get_put_delete_add_config_detail(request):
    """
    配置明细表
    """
    if request.method == "GET":
        with transaction.atomic():
            parser = FormatJsonParser(request)
            try:
                offset = parser.offset
                limit = parser.limit
                config_id = parser.config_id
                detail_id = parser.id
                
                # 通过配置表的id主键进行查询
                if config_id:
                    config = ConfigTable.get_config_by_id(id=config_id)
                    detail_list = config.detail_table.all()[offset:limit + offset]
                    serializer = ConfigDetailGetterSerializer(detail_list, many=True)
                
                # 通过配置明细表的id进行查询
                elif detail_id:
                    if isinstance(detail_id, list):
                        detail = ConfigDetailTable.objects.filter(id__in=detail_id)
                        serializer = ConfigDetailGetterSerializer(detail, many=True)
                    else:
                        detail = ConfigDetailTable.objects.get(id=detail_id)
                        serializer = ConfigDetailGetterSerializer(detail)
                    return SuccessJsonResponse(data=serializer.data)
                # 查询所有
                else:
                    detail = ConfigDetailTable.objects.all()
                    serializer = ConfigDetailGetterSerializer(detail, many=True)
                
                return SuccessJsonResponse(data=serializer.data)
                        

            except Exception as e:
                return ErrorJsonResponse(data=u"{0}".format(e))

    elif request.method == "POST":
        with transaction.atomic():
            parser = FormatJsonParser(request)
            data = parser.get_data()
            serializer = ConfigDetailPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return SuccessJsonResponse(data=serializer.data)
            else:
                return ErrorJsonResponse(data=serializer.errors)

    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        return ErrorJsonResponse("unsupported http method")

