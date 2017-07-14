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

    def get_content(self):
        content = u'\t'.join(map(unicode, [self.mac_addr, self.static_ip])) + u'\r'
        return content

    class Meta:
        ordering = ('mac_addr',)

class CnIpcChangeLogDetail(models.Model):
    """
    每个被改变的IPC的详细记录
    """
    #对应批量操作的任务ID
    operate_id = models.CharField(max_length=20)
    #对应MAC-IPC表中的ID
    ipc_id = models.IntegerField(max_length=10)

    mac_addr = models.CharField(max_length=16)
    static_ip = models.IPAddressField()
    osd_text = models.CharField(max_length=40, blank=True)
    ori_ip = models.IPAddressField()
    # status = models.IntegerField(max_length=5, choices={(1, u'设置IP到.60'),(2, u'恢复出厂成功'),
    #                                                     (3, u'设置IP到指定地址'),
    #                                                     (4, u'设置OSD成功')})
    status = models.IntegerField(max_length=5)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.mac_addr

    class Meta:
        ordering = ('static_ip','create_time')


class CnIpcOperateInfo(models.Model):
    """
    操作记录表格
    """
    operator_name = models.CharField(max_length=20)
    operate_type=models.IntegerField(max_length=2)
    create_time = models.DateTimeField(auto_now_add=True)
    #操作批次ID,以time.time()整数位为id
    operate_id = models.CharField(max_length=20,)
    ip_start = models.IPAddressField()
    ip_count = models.IntegerField(max_length=3)
    progress = models.IntegerField(max_length=3, default=0)

    def __unicode__(self):
        return self.operate_id + u'|' + self.operator_name

    class Meta:
        ordering = ('create_time',)

class CnRemoteTerminal(models.Model):
    """
    远程终端注册
    """
