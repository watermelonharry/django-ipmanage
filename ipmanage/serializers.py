# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *


class ConfigGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigTable
        fields = ("id", "config_name", "config_info", "config_count", "config_bind_topo", "user_name", "editor_name")


class ConfigPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigTable
        fields = ("config_name", "config_info", "config_count", "config_bind_topo", "user_name", "editor_name")


class ConfigPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigTable
        fields = ("id", "config_name", "config_info", "config_count", "config_bind_topo", "user_name", "editor_name")


class ConfigDetailGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigDetailTable
        fields = (
            "id", "mac_addr", "ori_ip", "set_ip", "ori_password", "set_password", "device_type", "device_firmware",
            "device_osd", "other_info", "creator_name", "edit_time")


class ConfigDetailPostSerializer(serializers.ModelSerializer):
    config_table_key = serializers.PrimaryKeyRelatedField(blank=True)

    class Meta:
        model = ConfigDetailTable
        exclude = ("edit_time", "create_time", "lock")