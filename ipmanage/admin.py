from django.contrib import admin

# Register your models here.
from ipmanage.models import *

admin.site.register(ConfigTable)
admin.site.register(ConfigDetailTable)
admin.site.register(MissionTable)
admin.site.register(MissionDetailTable)