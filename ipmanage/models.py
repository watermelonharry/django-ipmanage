# -*- coding: utf-8 -*-
from django.db import models, transaction


class ConfigTable(models.Model):
    """
    MAC-IP配置略表
    """
    config_name = models.CharField(max_length=30, null=False, unique=True)
    config_info = models.TextField(null=True, blank=True)

    config_count = models.IntegerField(blank=True, null=True)
    config_bind_topo = models.CharField(max_length=30, null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    editor_name = models.CharField(max_length=20, blank=True)
    user_name = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return u"{0}-{1}-{2}".format(self.id, self.config_name, self.editor_name)

    class Meta():
        ordering = ('-id',)


class ConfigDetailTable(models.Model):
    """
    MAC-IP配置明细表
    """
    config_table_key = models.ForeignKey(ConfigTable, on_delete=models.CASCADE)

    mac_addr = models.CharField(max_length=16, blank=True)

    ori_ip = models.IPAddressField(blank=True, null=True)
    set_ip = models.IPAddressField(blank=True, null=True)

    ori_password = models.CharField(max_length=32, blank=True, null=True)
    set_password = models.CharField(max_length=32, blank=True, null=True)

    # 样机类型
    device_type = models.CharField(max_length=50, blank=True, null=True)
    device_firmware = models.CharField(max_length=50, blank=True, null=True)
    device_osd = models.CharField(max_length=40, blank=True, null=True)

    other_info = models.TextField(max_length=200, blank=True, null=True)

    # lock this record: 1-lock, 0-editable
    lock = models.IntegerField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    editor_name = models.CharField(max_length=20, blank=True, null=True)
    creator_name = models.CharField(max_length=20, blank=True)


    def __unicode__(self):
        return "{0}-{1}-{2}".format(self.mac_addr, self.set_ip, self.editor_name)

    def get_content(self):
        content = u'\t'.join(map(unicode, [self.mac_addr, self.ori_ip, self.ori_password])) + u'\r'
        return content

    @classmethod
    def get_config_by_mac(cls, mac_addr):
        try:
            record = cls.objects.get(mac_addr=mac_addr)
            return record
        except Exception as e:
            return None

    class Meta:
        ordering = ("config_table_key", "id",)
        unique_together = (("config_table_key", "mac_addr"),)


class MissionTable(models.Model):
    """
    任务简表
    """
    MISSION_TYPE_CHOICE = ((0, u"自动扫描并添加"), (1, u"执行恢复操作"))
    MISSION_STATUS_CHOICE = ((0, u"终止"), (1, u"等待"), (2, u"运行"), (3, u"完成"), (11, u"异常"))

    # 0:auto scan, 1:restore and set

    mission_type = models.IntegerField(choices=MISSION_TYPE_CHOICE, blank=True)

    start_ip = models.IPAddressField(blank=True, null=True)
    total_count = models.IntegerField(max_length=3, blank=True, null=True)
    progress = models.IntegerField(max_length=3, blank=True, null=True)

    run_status = models.IntegerField(choices=MISSION_STATUS_CHOICE, null=True, blank=True)
    run_info = models.TextField(null=True, blank=True)

    # assigned terminal's name
    terminal_name = models.CharField(max_length=40, blank=True, null=True)

    user_name = models.CharField(max_length=20, blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"{0}-{1}-{2}".format(self.id, self.mission_type, self.user_name)

    class Meta:
        ordering = ('-id',)

    @classmethod
    def get_mission_by_id(cls, mid):
        try:
            mission = cls.objects.get(mission_id=mid)
            return mission
        except Exception as e:
            return None


class MissionDetailTable(models.Model):
    """
    任务明细表
    """
    MISSION_DETAIL_RUN_STATUS_CHOICE = ((0, u"终止"), (1, u"等待"), (2, u"运行"), (3, u"完成"), (11, u"异常"))

    # 对应批量操作的任务ID
    mission_table_key = models.ForeignKey(MissionTable, on_delete=models.CASCADE)

    mac_addr = models.CharField(max_length=16, blank=True)
    ori_ip = models.IPAddressField(blank=True, null=True)
    set_ip = models.IPAddressField(blank=True, null=True)
    ori_password = models.CharField(max_length=32, blank=True, null=True)
    set_password = models.CharField(max_length=32, blank=True, null=True)

    # 样机类型
    device_type = models.CharField(max_length=50, blank=True, null=True)
    device_firmware = models.CharField(max_length=50, blank=True, null=True)
    device_osd = models.CharField(max_length=40, blank=True, null=True)

    other_info = models.TextField(max_length=200, blank=True, null=True)

    detail_run_status = models.IntegerField(choices=MISSION_DETAIL_RUN_STATUS_CHOICE, blank=True, null=True)
    detail_run_info = models.TextField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return u"{0}-{1}-{2}".format(self.mission_table_key.id, self.mac_addr, self.set_ip)

    class Meta:
        ordering = ('-mission_table_key',)

    @classmethod
    def get_detail_by_id(cls, detail_id):
        """
        通过id 获取唯一的mission_detail对象
        :param detail_id (int):
        :return: None/ MissionDetailTabled实例
        """
        try:
            detail_obj= cls.objects.get(id=detail_id)
            return detail_obj
        except Exception as e:
            return None


