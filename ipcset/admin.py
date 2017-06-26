# -*- coding: utf-8 -*-
from django.contrib import admin

from ipcset.models import *

admin.site.register(BaseMacTable)
admin.site.register(BaseResolutionTable)
admin.site.register(BaseFramerateTable)
admin.site.register(BaseBitrateTable)
admin.site.register(BaseTypeTable)

admin.site.register(MissionInfoTable)
admin.site.register(MissionDetailTable)
admin.site.register(VideoSettingTable)