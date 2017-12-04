# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class BaseResolutionTable(models.Model):
    """
    分辨率表格
    """
    resolution = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return unicode(self.resolution)

    def get_resolution(self):
        return unicode(self.resolution)

    class Meta:
        ordering = ('id',)


class BaseBitrateTable(models.Model):
    """
    码率表格
    """
    bitrate = models.IntegerField(max_length=10, unique=True)

    def __unicode__(self):
        return unicode(self.bitrate)

    def get_bitrate(self):
        return unicode(self.bitrate)


class BaseFramerateTable(models.Model):
    """
    帧率表
    """
    framerate = models.IntegerField(max_length=2, unique=True)

    def __unicode__(self):
        return unicode(self.framerate)

    def get_framerate(self):
        return unicode(self.framerate)


# class BaseUserTable(models.Model):
#     pass

class BaseTypeTable(models.Model):
    """
    设备型号表
    """
    model_name = models.CharField(max_length=20, unique=True)
    alias_name = models.CharField(max_length=30, unique=True, blank=True)
    resolution_set = models.ManyToManyField(BaseResolutionTable)
    bitrate_set = models.ManyToManyField(BaseBitrateTable)
    framerate_set = models.ManyToManyField(BaseFramerateTable)

    min_resolution_set = models.ManyToManyField(BaseResolutionTable, related_name='min_reso_set')
    min_bitrate_set = models.ManyToManyField(BaseBitrateTable, related_name='min_bitrate_set')
    min_framerate_set = models.ManyToManyField(BaseFramerateTable, related_name='min_framerate_set')

    editor_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.model_name)

    def get_content(self):
        # todo:
        pass

    def get_model_name(self):
        return unicode(self.model_name)

    class Meta:
        ordering = ('id',)

    @classmethod
    def get_param_by_alias(cls, alias_name):
        """
        get the params of the model by the given alias name
        :param alias_name: eg. "323"
        :return: instance of BaseTypeTable or {}
        """
        try:
            return cls.objects.get(alias_name=alias_name)
        except Exception as e:
            raise e


class VideoSettingTable(models.Model):
    """
    设置表
    """
    mac_addr = models.CharField(max_length=16)
    current_ip = models.IPAddressField()
    type_id = models.ForeignKey(BaseTypeTable)

    set_resolution = models.CharField(max_length=20)
    set_bitrate = models.IntegerField(max_length=10)
    set_framerate = models.CharField(max_length=20)

    set_min_resolution = models.CharField(max_length=20)
    set_min_bitrate = models.IntegerField(max_length=10)
    set_min_framerate = models.CharField(max_length=20)
    # 操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示
    operate_type = models.IntegerField(max_length=2, default=2)

    editor_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    status = models.IntegerField(max_length=1, default=0)

    # cbr:cbr    vbr: low, medium, high
    set_cbr = models.CharField(max_length=10, null=True,blank=True)
    set_min_cbr = models.CharField(max_length=10, null=True,blank=True)
    # h264, h265
    set_code_type = models.CharField(max_length=10, null=True,blank=True)
    set_min_code_type = models.CharField(max_length=10, null=True,blank=True)
    # username
    user_name = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.mac_addr)

    @classmethod
    def get_settings_by_username(cls, user_name):
        try:
            return cls.objects.filter(user_name=user_name)
        except Exception as e:
            return []

    def get_download_content(self):
        return u','.join(map(unicode, [self.edit_time.strftime('%Y-%m-%d %H:%M:%S'),
                                       self.mac_addr, self.current_ip, self.type_id.model_name,
                                       self.set_resolution, self.set_bitrate, self.set_framerate,
                                       self.set_min_resolution, self.set_min_bitrate, self.set_min_framerate,
                                       self.editor_name])) + u'\n'

    class Meta:
        ordering = ('id',)


class MissionInfoTable(models.Model):
    """
    任务简表
    """
    # todo: progress的default = 0会被终止的post(不带progress)影响
    mission_id = models.CharField(max_length=20, unique=True)
    total_count = models.IntegerField(max_length=5, blank=True)
    progress = models.IntegerField(max_length=5, blank=True)

    remote_id = models.CharField(max_length=20, blank=True)
    editor_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    start_ip = models.IPAddressField(blank=True)
    # running flag, 1: run,  0: terminate
    run_status = models.IntegerField(max_length=1, blank=True)

    ##任务类型，1：设置设备  2：发现设备
    mission_type = models.IntegerField(max_length=2, blank=True)
    user_name = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.mission_id)

    def get_content(self):
        # todo:
        pass

    class Meta:
        ordering = ('-create_time',)

    @classmethod
    def get_missions_by_terminal(cls, terminal_name):
        try:
            terminal_list = cls.objects.filter(remote_id=terminal_name)
            return terminal_list
        except Exception as e:
            return []


class MissionDetailTable(models.Model):
    """
    任务明细表
    """
    mission_id = models.CharField(max_length=20)

    mac_addr = models.CharField(max_length=16)
    current_ip = models.IPAddressField()
    type_id = models.ForeignKey(BaseTypeTable)

    set_resolution = models.CharField(max_length=20)
    set_bitrate = models.IntegerField(max_length=10)
    set_framerate = models.CharField(max_length=20)

    set_min_resolution = models.CharField(max_length=20)
    set_min_bitrate = models.IntegerField(max_length=10)
    set_min_framerate = models.CharField(max_length=20)
    # 操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示
    operate_type = models.IntegerField(max_length=2, default=1)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    ##0: 等待设置，  3：设置失败  5：设置成功     1：已更新 2：已添加
    status = models.IntegerField(max_length=1, default=0)

    # cbr:cbr    vbr: low, medium, high
    set_cbr = models.CharField(max_length=10, null=True,blank=True)
    set_min_cbr = models.CharField(max_length=10, null=True,blank=True)
    # h264, h265
    set_code_type = models.CharField(max_length=10, null=True,blank=True)
    set_min_code_type = models.CharField(max_length=10, null=True,blank=True)
    # username
    user_name = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.current_ip)

    def get_content(self):
        # todo:
        pass

    class Meta:
        ordering = ('current_ip',)

    @classmethod
    def get_mission_detail_by_mission_id(cls, mission_id):
        try:
            return cls.objects.filter(mission_id=mission_id)
        except Exception as e:
            return []