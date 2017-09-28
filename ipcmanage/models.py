# -*- coding: utf-8 -*-
from django.db import models


class StaticIpMacTable(models.Model):
    """
    默认的IPC-IP对应表格
    """
    mac_addr = models.CharField(max_length=16)
    ori_ip = models.IPAddressField(blank=True, null=True)
    set_ip = models.IPAddressField(blank=True, null=True)

    ori_password = models.CharField(max_length=32,blank=True,null=True)
    set_password = models.CharField(max_length=32,blank=True,null=True)

    other_info = models.TextField(max_length=200, blank=True, null=True)

    # lock this record: 1-lock, 0-editable
    lock = models.IntegerField(blank=True, null=True)
    # device status: 1-newly added, 2-been edited, 3-refreshed
    status = models.IntegerField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    editor_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20, blank=True)

    # todo: 添加OSD等其他设置

    def __unicode__(self):
        return "{0}-{1}".format(self.mac_addr, self.user_name)

    def get_content(self):
        content = u'\t'.join(map(unicode, [self.mac_addr, self.ori_ip, self.ori_password])) + u'\r'
        return content

    @classmethod
    def get_record_by_mac(cls, mac_addr):
        try:
            record = cls.objects.get(mac_addr=mac_addr)
            return record
        except Exception as e:
            return None

    class Meta:
        ordering = ('-create_time',)


class IpMissionTable(models.Model):
    """
    mission table
    """
    mission_id = models.CharField(max_length=20, blank=True)

    # 0:auto scan, 1:restore and set
    mission_type = models.IntegerField(max_length=2, blank=True)
    # mission_ID,以time.time()整数位为id
    start_ip = models.IPAddressField(blank=True, null=True)
    total_count = models.IntegerField(max_length=3, blank=True, null=True)
    progress = models.IntegerField(max_length=3, blank=True, null=True)

    # 0-terminated, 1-normal, 2-scanning done, setting done
    run_status = models.IntegerField(max_length=1, blank=True)
    remote_id = models.CharField(max_length=30,blank=True,null=True)

    user_name = models.CharField(max_length=20, blank=True, null=True)
    editor_name = models.CharField(max_length=20)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.operate_id + u'-' + self.operator_name

    class Meta:
        ordering = ('-create_time',)

    @classmethod
    def get_mission_by_mission_id(cls, mid):
        try:
            mission = cls.objects.get(mission_id=mid)
            return mission
        except Exception as e:
            return []


class IpMissionDetailTable(models.Model):
    """
    每个被改变的IPC的详细记录
    """
    # 对应批量操作的任务ID
    mission_id = models.CharField(max_length=20)

    mac_addr = models.CharField(max_length=16)
    ori_ip = models.IPAddressField(blank=True, null=True)
    set_ip = models.IPAddressField(blank=True, null=True)

    ori_password = models.CharField(max_length=32, blank=True, null=True)
    set_password = models.CharField(max_length=32, blank=True, null=True)

    other_info = models.TextField(max_length=200, blank=True, null=True)

    # device status: 1-newly added, 2-been edited, 3-refreshed
    status = models.IntegerField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    editor_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.mac_addr

    class Meta:
        ordering = ('-create_time', 'mission_id')
