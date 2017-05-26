# -*- coding: utf-8 -*-


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
import datetime
from forms import CnTestSubscribeForm


def case_list(request):
    case_list = CnCaseInfo.objects.all()
    secondTitle = u'查看用例信息'
    for case in case_list:
        case.suiteName = CnTestSuiteList.objects.filter(id = case.testSuiteId)[0].suiteName
    return render_to_response('dns_case_info.html', locals())


def tester_list(request):
    tester_list = CnTestEngieer.objects.all()
    secondTitle = u'查看测试人员'
    return render_to_response('dns_tester_info.html',locals())


def subs_list(request):
    if request.method == 'POST':
        status = request.POST.get('status',None)
        subId = request.POST.get('subId',None)
        if status is not None and subId is not None:
            subTarget = CnTestSubscribeList.objects.filter(id = subId)[0]
            subTarget.testStatus = status
            subTarget.save()

    plan_list = CnTestSubscribeList.objects.all()
    case_id_lst = map(lambda y:[x.id for x in y.testCaseId.all()], plan_list)
    case_id_lst = map(lambda x:'|'.join([str(y) for y in x]), case_id_lst)
    for plan, id_str in zip(plan_list, case_id_lst):
        plan.case_str = id_str
    secondTitle = u'查看预约任务'
    return render_to_response('dns_testplan.html', locals())


def operate_list(request):
    pass


def testsuite_list(request, suiteId=None):
    if suiteId is None:
        suite_list = CnTestSuiteList.objects.all()
        secondTitle = u'查看测试集合'
        return render_to_response('dns_testsuite_info.html', locals())

    else:
        case_list = CnCaseInfo.objects.all().filter(testSuiteId=suiteId).order_by('id')
        secondTitle = CnTestSuiteList.objects.filter(id=suiteId)[0].suiteName
        for case in case_list:
            case.suiteName = secondTitle
        secondTitle = u'用例集合：'+secondTitle
        return render_to_response('dns_case_info.html', locals())

def new_test_plan(request):
    secondTitle = u'新建测试计划'
    if request.method == 'POST':
        form = CnTestSubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('dns_subscribe_success.html',locals())
    else:
        form = CnTestSubscribeForm
    return render_to_response('dns_new_plan.html', locals())