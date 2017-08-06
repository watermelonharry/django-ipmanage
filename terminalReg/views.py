# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from jsonreformat import *

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
		new_terminal = TerminalModelSerializer(old_terminal, data=data)
	except Exception as e:
		new_terminal = TerminalModelSerializer(data=data)

	if new_terminal.is_valid():
		new_terminal.save()
		return SuccessJsonResponse(data={'user': user_model.username, 'ak': terminal_ak}, status=200)
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
def api_get_online_terminal_list(request):
	#todo: ak verify
	terminal_list = map(lambda x:x if x.is_online() is True else None, TerminalModel.objects.all())
	data = TerminalModelSerializer(data=terminal_list, many=True)
	return SuccessJsonResponse(data=data)