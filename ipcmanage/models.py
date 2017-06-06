# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class CnTestEngieer(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    cardNo = models.CharField(max_length=20)
    emailAddr = models.EmailField()
    type = models.IntegerField()

    def __unicode__(self):
        return self.name

class CnStaticIpcTable(models.Model):
    """
    默认的IPC-IP对应表格
    """
    mac_addr = models.CharField(max_length=16)
    static_ip = models.IPAddressField(blank=True)
    osd_text = models.CharField(max_length=40, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    editor_name = models.CharField(max_length=20)
    #todo: 添加OSD等其他设置

    def __unicode__(self):
        return self.mac_addr

class CnTempIpcTable(models.Model):
    """
    临时文件的IPC-IP对应表格
    """
    mac_addr = models.CharField(max_length=16)
    static_ip = models.IPAddressField(blank=True)
    osd_text = models.CharField(max_length=40, blank=True)
    #todo: 添加OSD等其他设置
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    editor_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.mac_addr


class CnIpcOperateInfo(models.Model):
    """
    操作记录表格
    """
    operator_name = models.CharField(max_length=20)
    operate_type=models.IntegerField(max_length=2, choices=((1, u'添加IPC'),
                                                            (2, u'删除IPC'),
                                                            (3, u'修改IPC')))
    changed_ipc_mac = models.TextField(blank=True)
    change_time = models.DateTimeField(auto_now_add=True)
    #操作批次ID,以time.time()整数位为id
    operate_hash_id = models.CharField(max_length=20)

    def __unicode__(self):
        return self.operate_hash_id + u'|' + self.operator_name

