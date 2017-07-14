# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class BaseFrameSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseFramerateTable
		fields = ('id', 'framerate')


class BaseBitrateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseBitrateTable
		fields = ('id', 'bitrate')


class BaseResolutionSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseResolutionTable
		fields = ('id', 'resolution')


class BaseTypeSerializer(serializers.ModelSerializer):
	resolution_set = BaseResolutionSerializer(many=True, read_only=True)
	framerate_set = BaseFrameSerializer(many=True, read_only=True)
	bitrate_set = BaseBitrateSerializer(many=True, read_only=True)

	min_resolution_set = BaseResolutionSerializer(many=True, read_only=True)
	min_framerate_set = BaseFrameSerializer(many=True, read_only=True)
	min_bitrate_set = BaseBitrateSerializer(many=True, read_only=True)

	class Meta:
		model = BaseTypeTable
		fields = ('id', 'model_name', 'alias_name',
		          'resolution_set', 'bitrate_set', 'framerate_set',
		          'min_resolution_set', 'min_bitrate_set', 'min_framerate_set',
		          'editor_name')


class VideoSettingSerializer(serializers.ModelSerializer):
	type_id = BaseTypeSerializer(read_only=True)

	class Meta:
		model = VideoSettingTable
		fields = ('id', 'mac_addr', 'current_ip', 'type_id',
		          'set_resolution', 'set_bitrate', 'set_framerate',
		          'set_min_resolution', 'set_min_bitrate', 'set_min_framerate',
		          'operate_type',
		          'status', 'editor_name')
	# 操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示


class VideoSettingPartSerializer(serializers.ModelSerializer):
	class Meta:
		model = VideoSettingTable
		fields = ('set_resolution', 'set_bitrate', 'set_framerate',
		          'set_min_resolution', 'set_min_bitrate', 'set_min_framerate',
		          'operate_type', 'editor_name')


class MissionDetailSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MissionDetailTable
		fields = ('id', 'mission_id', 'mac_addr', 'current_ip',
		          'set_resolution', 'set_bitrate', 'set_framerate',
		          'set_min_resolution', 'set_min_bitrate', 'set_min_framerate',
		          'status', 'operate_type'
		          )


class MissionInfoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MissionInfoTable
		##任务类型，1：设置设备  2：发现设备
		fields = ('id', 'mission_id', 'total_count', 'progress', 'run_status', 'start_ip', 'editor_name', 'remote_id',
		          'mission_type')
