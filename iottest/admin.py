from django.contrib import admin
from models import IotDeviceTable,MissionDetailTable,MissionTable
# Register your models here.


admin.site.register(IotDeviceTable)
admin.site.register(MissionTable)
admin.site.register(MissionDetailTable)
