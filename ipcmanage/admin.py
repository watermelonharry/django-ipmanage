# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from ipcmanage.models import *

admin.site.register(IpMissionTable)
admin.site.register(StaticIpMacTable)
admin.site.register(CnIpcChangeLogDetail)
admin.site.register(CnTestEngieer)
admin.site.register(CnRemoteTerminal)