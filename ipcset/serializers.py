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
    frametrate_set = BaseFrameSerializer(many=True, read_only=True)
    bitrate_set = BaseBitrateSerializer(many=True, read_only=True)
    class Meta:
        model = BaseTypeTable
        fields = ('id', 'model_name', 'alias_name',
                  'resolution_set', 'bitrate_set',
                  'framerate_set', 'editor_name')


class VideoSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSettingTable
        fields = ('id', 'mac_addr','current_ip', 'type_id',
                  'set_resolution', 'set_bitrate','set_framerate','operate_type',
                  'status','editor_name')
        # 操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示


class MissionDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissionDetailTable
        fields = ('id','mission_id','mac_addr','current_ip',
                  'set_resolution','set_bitrate','set_framerate',
                  'status','operate_type')


class MissionInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissionInfoTable
        fields = ('id','mission_id', 'total_count', 'progress')
