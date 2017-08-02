# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from jsonreformat import *
from serializers import *

from userManage.models import ApiKeyModel, UserApiModel


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
    terminal_ak = data.get('ak', '')
    api_model = ApiKeyModel.has_record(terminal_ak)
    if api_model is None:
        return ErrorJsonResponse(data={'ak':'un verified ak'}, status=400)

    user_model = UserApiModel.objects.get(id=api_model.user_id)
    terminal_name = data.get('terminal_name', None)
    if terminal_name is None:
        return ErrorJsonResponse(data={'teminal_name':'is null'},status=400)

    try:
        old_terminal = TerminalModel.objects.get(terminal_name=terminal_name)
        new_terminal = TerminalModelSerializer(old_terminal,data=data)
    except Exception as e:
        new_terminal = TerminalModelSerializer(data=data)

    if new_terminal.is_valid():
        new_terminal.save()
        return SuccessJsonResponse(data={'user': user_model.username, 'ak': terminal_ak}, status=200)
    else:
        return ErrorJsonResponse(data=new_terminal.errors)
