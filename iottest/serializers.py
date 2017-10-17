# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class IotDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotDeviceTable
        fields = ('id', 'device_name', 'device_type',
                  'device_addr', 'device_username', 'device_ov_password', 'device_web_password',
                  'device_software_version',
                  'other_info', 'editor_name', 'edit_time')


class MissionTableGetSerializer(serializers.ModelSerializer):
    # sut_ids = serializers.PrimaryKeyRelatedField(many=True, blank=True)
    sut_ids = IotDeviceSerializer(many=True, blank=True)
    class Meta:
        model = MissionTable
        fields = ('id', 'dut_name', 'dut_version', 'dut_addr',
                  'dut_type', 'dut_username', 'dut_password', 'dut_cmp_lock', 'other_info', 'editor_name', "sut_ids",
                  'mission_status', 'create_time','terminal_name','mission_total')

class MissionTablePostSerializer(serializers.ModelSerializer):
    sut_ids = serializers.PrimaryKeyRelatedField(many=True, blank=True)
    class Meta:
        model = MissionTable
        fields = ('id', 'dut_name', 'dut_version', 'dut_addr',
                  'dut_type', 'dut_username', 'dut_password', 'dut_cmp_lock', 'other_info', 'editor_name', "sut_ids",
                  'mission_status', 'create_time','terminal_name','username','mission_total')

class MissionDetailGetSerializer(serializers.ModelSerializer):
    mission_id = serializers.PrimaryKeyRelatedField(blank=True)
    # iot_device_id = serializers.PrimaryKeyRelatedField(blank=True)
    iot_device_id = IotDeviceSerializer(blank=True)

    class Meta:
        model = MissionDetailTable
        exclude = ('edit_time',)

class MissionDetailPostSerializer(serializers.ModelSerializer):
    mission_id = serializers.PrimaryKeyRelatedField(blank=True)
    iot_device_id = serializers.PrimaryKeyRelatedField(blank=True)
    # iot_device_id = IotDeviceSerializer(blank=True)

    class Meta:
        model = MissionDetailTable
        exclude = ('edit_time',)
