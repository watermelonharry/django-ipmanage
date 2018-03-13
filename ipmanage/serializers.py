# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class ConfigGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigTable
        fields = ("id", "config_name", "config_info", "config_count", "config_bind_topo", "user_name")


class ConfigDetailGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigDetailTable
        fields = (
        "id", "mac_addr", "ori_ip", "set_ip", "ori_password", "set_password", "device_type", "device_firmware",
        "device_osd", "other_info", "creator_name", "edit_time")


# class IpMissionSerializer(serializers.ModelSerializer):
# class Meta:
#         model = IpMissionTable
#         fields = ('id', 'mission_id', 'mission_type', 'start_ip', 'total_count',
#                   'progress', 'run_status', 'user_name',
#                   'editor_name', 'edit_time')
#
#
# class IpMissionDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IpMissionDetailTable
#         fields = ('id', 'mission_id', 'mac_addr', 'ori_ip', 'set_ip', 'other_info',
#                   "ori_password", "set_password",
#                   'status', 'edit_time', 'editor_name', 'user_name')
