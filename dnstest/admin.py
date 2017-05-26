from django.contrib import admin

# Register your models here.
from dnstest.models import CnTestEngieer,CnCaseInfo,CnOperateInfo,CnTestSubscribeList,CnTestSuiteList

admin.site.register(CnTestEngieer)
admin.site.register(CnCaseInfo)
admin.site.register(CnOperateInfo)
admin.site.register(CnTestSubscribeList)
admin.site.register(CnTestSuiteList)

