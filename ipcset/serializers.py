# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class VideoSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoSettingTable
        fields = ('mac_addr_id','current_ip','set_resolution',
                  'set_bitrate','set_framerate','operate_type',
                  'editor_name','create_time','edit_time')
        # 操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示


class MissionDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissionDetailTable
        fields = ('mission_id','mac_id','ip_addr',
                  'set_resolution','set_bitrate','set_framerate',
                  'status')


class MissionInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissionInfoTable
        fields = ('mission_id', 'total_count', 'progress')
