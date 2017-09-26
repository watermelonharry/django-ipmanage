# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from ipcmanage.models import *

admin.site.register(StaticIpMacTable)
admin.site.register(IpMissionTable)
admin.site.register(IpMissionDetailTable)
