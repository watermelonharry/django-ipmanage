# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class TerminalModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TerminalModel
		fields = ('id', 'terminal_name', 'terminal_status',
		          'terminal_type', 'ak', 'user_name', 'terminal_addr', 'available_time',
				  'version',
		          'terminal_port', 'other_info', 'edit_time')


class TerminalHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = TerminalHistoryModel
		fields = ('id', 'terminal_id', 'mission_id', 'create_time')


class TerminalWaitingMissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TerminalWaitingMissionModel
		fields = ('id', 'terminal_name', 'mission_id', 'mission_from', 'mission_url', 'mission_status', 'edit_time')
