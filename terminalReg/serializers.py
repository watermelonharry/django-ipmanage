# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class TerminalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalModel
        fields = ('id', 'terminal_name', 'terminal_status',
                  'terminal_type', 'ak', 'terminal_addr',
                  'terminal_port','other_info','edit_time')


class TerminalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalHistoryModel
        fields = ('id', 'terminal_id', 'mission_id', 'create_time')
