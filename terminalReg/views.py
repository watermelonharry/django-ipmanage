# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from models import *


# Create your views here.

class TerminalListView(ListView):
	model = TerminalModel
	template_name = "terminal_list.html"

	pass
