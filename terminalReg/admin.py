from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(TerminalModel)
admin.site.register(TerminalHistoryModel)
admin.site.register(TerminalWaitingMissionModel)