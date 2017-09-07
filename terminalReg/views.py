# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from basepkg.jsonreformat import *

from userManage.models import ApiKeyModel, UserApiModel
from serializers import *


# Create your views here.

class TerminalListView(ListView):
    model = TerminalModel
    template_name = "terminal_list.html"

    @method_decorator(login_required)
    def get(self, request):
        """
        show terminals
        """
        terminal_list = TerminalModel.objects.all()
        return render(request, self.template_name, {'firstTitle': u'终端管理',
                                                    'firstTitle_content': u'',
                                                    'terminal_list': terminal_list})


class TerminalRegister(DetailView):
    model = TerminalModel

    @csrf_exempt
    def post(self, request):
        """
        terminal register by POST to this url
        """
        data = JSONParser().parse(request)
        terminal_ak = data.get('ak', '')
        api_model = ApiKeyModel.has_record(terminal_ak)
        user_model = UserApiModel.objects.get(id=api_model.user_id)

        return SuccessJsonResponse(data={'user': 'user_model.username', 'ak': terminal_ak}, status=200)


@csrf_exempt
def api_temrinal_register_post(request):
    """
    terminal register by POST to this url with{ak, terminal_name}
    """
    # todo: register with ak,terminal_name,and so on
    data = JSONParser().parse(request)
    terminal_addr = request.META.get('REMOTE_ADDR', '')
    terminal_ak = data.get('ak', '')
    api_model = ApiKeyModel.has_record(terminal_ak)
    if api_model is None:
        return ErrorJsonResponse(data={'ak': 'un verified ak'}, status=400)

    user_model = UserApiModel.objects.get(id=api_model.user_id)
    terminal_name = data.get('terminal_name', None)
    if terminal_name is None:
        return ErrorJsonResponse(data={'teminal_name': 'is null'}, status=400)

    try:
        old_terminal = TerminalModel.objects.get(terminal_name=terminal_name)
        old_terminal.update_data(user_name=user_model.username)
        new_terminal = TerminalModelSerializer(old_terminal, data=data)
    except Exception as e:
        data.update({'user_name':user_model.username})
        new_terminal = TerminalModelSerializer(data=data)

    if new_terminal.is_valid():
        new_terminal.save()

        try:
            waiting_mission = TerminalWaitingMissionModel.get_mission_by_terminal_name(terminal_name)
            m_serializer = TerminalWaitingMissionSerializer(waiting_mission)
            mission_info = m_serializer.data
        except Exception as e:
            mission_info = {}

        reply_dict = {'user': user_model.username, 'ak': terminal_ak}
        reply_dict.update(mission_info)

        return SuccessJsonResponse(data=reply_dict,
                                   status=200)
    else:
        return ErrorJsonResponse(data=new_terminal.errors)


class InnerApiBindMissionTerminal(DetailView):
    # @method_decorator(csrf_exempt)
    def post(self, request):
        """
        api to bind the mission with terminal
        """
        format_data = FormatJsonParser(request)
        if TerminalModel.has_terminal(format_data.get_terminal_name()) is False:
            return ErrorJsonResponse(data={"terminal_name": "terminal not found"}, status=400)

        data = format_data.get_content()
        new_bind = TerminalWaitingMissionSerializer(data=data)
        if new_bind.is_valid() is True:
            new_bind.save()
            return SuccessJsonResponse(data=data, status=200)
        else:
            return ErrorJsonResponse(data=new_bind.errors, status=406)


@csrf_exempt
def api_outer_get_online_terminal_list(request):
    """
    outer API for ?? to get online_terminals
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        api_model = ApiKeyModel.has_ak(data)
        if api_model:
            online_list = TerminalModel.get_online_list()
            terminal_data = TerminalModelSerializer(online_list, many=True).data
            return SuccessJsonResponse(data=terminal_data)
        else:
            return ErrorJsonResponse(data={"ak": "invalid ak"}, status=411)


class InnerApiGetOnlineTerminal(ListView):
    """
    inner API for users to get online terminal_list
    """
    model = TerminalModel

    @method_decorator(login_required)
    def get(self, request):
        online_list = TerminalModel.get_online_list()
        data = TerminalModelSerializer(online_list, many=True).data
        return SuccessJsonResponse(data=data)
