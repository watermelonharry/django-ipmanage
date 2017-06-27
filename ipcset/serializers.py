# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class VideoSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSettingTable
        fields = ('id', 'mac_addr','current_ip', 'type_id',
                  'set_resolution', 'set_bitrate','set_framerate','operate_type',
                  'editor_name')
        # 操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示


class MissionDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissionDetailTable
        fields = ('mission_id','mac_addr','ip_addr',
                  'set_resolution','set_bitrate','set_framerate',
                  'status')


class MissionInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissionInfoTable
        fields = ('mission_id', 'total_count', 'progress')
