# -*- coding: utf-8 -*-


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *

def welcome(request):
    return render_to_response('ipc_hello.html',{'firstTitle':u'IPC批量IP设置工具',
                                                  'firstTitle_content':u'批量管理IPC的IP地址'})

def show_ip_table(request):
    ip_list = CnStaticIpcTable.objects.all()
    return render_to_response('ipc_mac_ip_table.html',{'firstTitle':u'IPC批量IP设置工具',
                                                       'firstTitle_content':u'批量管理IPC的IP地址',
                                                       'ip_list':ip_list})