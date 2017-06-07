# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import *

# class CnStaticIpTableSerializer(serializers.Serializer):
#     mac_addr = serializers.CharField(required=True, max_length=16)
#     static_ip = serializers.IPAddressField(required=True)
#     osd_text = serializers.CharField(max_length=40, blank=True)
#     editor_name = serializers.CharField(required=True, max_length=20)
#
#     create_time = serializers.IntegerField(read_only=True)
#     edit_time = serializers.DateTimeField(read_only=True, auto_now=True)
#
#
#     def create(self, validated_data):
#         '''
#         如果数据合法，就创建并返回一个新的Cn实例
#         '''
#         return CnStaticIpcTable.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         '''
#         如果数据合法，就更新并返回一个已经存在的Snippet实例
#         '''
#         instance.mac_addr = validated_data.get('mac_addr',instance.mac_addr)
#         instance.static_ip = validated_data.get('static_ip',instance.static_ip)
#         instance.osd_text = validated_data.get('osd_text',instance.osd_text)
#         instance.editor_name = validated_data.get('editor_name',instance.editor_name)
#         instance.save()
#         return instance


class CnStaticIpTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CnStaticIpcTable
        fields = ('id','mac_addr','static_ip','osd_text','editor_name')