# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator


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
		return render(self.template_name, {'firstTitle':u'在线终端查看',
										   'firstTitle_content':u'',
										   'terminal_list':terminal_list})

