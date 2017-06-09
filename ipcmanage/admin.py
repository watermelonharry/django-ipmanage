# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from ipcmanage.models import *

admin.site.register(CnIpcOperateInfo)
admin.site.register(CnStaticIpcTable)
admin.site.register(CnIpcChangeLogDetail)
