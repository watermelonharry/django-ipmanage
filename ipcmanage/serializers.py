# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class StaticIpMacTableSerializer(serializers.ModelSerializer):
	class Meta:
		model = StaticIpMacTable
		fields = ('id', 'mac_addr', 'static_ip', 'osd_text', 'editor_name')


class CnOperateInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = IpMissionTable
		fields = ('id', 'operate_id', 'operator_name', 'operate_type', 'run_status', 'ip_start', 'ip_count', 'progress')


class CnIpcLogDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = CnIpcChangeLogDetail
		fields = ('id', 'operate_id', 'ipc_id', 'mac_addr', 'static_ip', 'osd_text', 'ori_ip', 'status', 'edit_time')
