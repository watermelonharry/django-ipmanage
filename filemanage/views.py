# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from userManage.models import ApiKeyModel, UserApiModel
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse


# from django.db.models.fields.related




# from django.contrib.auth.models import User

@login_required
def show_file_main_page(request):
    return render_to_response('file_main_page.html', {'firstTitle': u'文件下载',
                                                      'firstTitle_content': u'-必要文件下载'},
                              context_instance=RequestContext(request))


@login_required
def download_terminal_package(request):
    k = open(r"D:\Code\testdown.zip", 'rb')
    response = StreamingHttpResponse(k.readlines(), content_type='APPLICATION/OCTET=STREAM')
    response['Content-Disposition'] = 'attachment; filename=testdown.zip'
    return response
