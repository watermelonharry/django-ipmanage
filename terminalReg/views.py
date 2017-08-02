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
	terminal register by POST to this url
	"""
	#todo: register with ak,terminal_name,and so on
	data = JSONParser().parse(request)
	terminal_ak = data.get('ak', '')
	api_model = ApiKeyModel.has_record(terminal_ak)
	user_model = UserApiModel.objects.get(id=api_model.user_id)

	return SuccessJsonResponse(data={'user': user_model.username, 'ak': terminal_ak}, status=200)