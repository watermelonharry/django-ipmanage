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
    bitrate = models.IntegerField(max_length=10,unique=True)

    def __unicode__(self):
        return unicode(self.bitrate)

    def get_bitrate(self):
        return unicode(self.bitrate)

class BaseFramerateTable(models.Model):
    """
    帧率表
    """
    framerate = models.IntegerField(max_length=2,unique=True)

    def __unicode__(self):
        return unicode(self.framerate)

    def get_framerate(self):
        return unicode(self.framerate)

# class BaseUserTable(models.Model):
#     pass

class BaseTypeTable(models.Model):
    """
    IPC型号表
    """
    model_name = models.CharField(max_length=20,unique=True)
    alias_name = models.CharField(max_length=30, unique=True, blank=True)
    resolution_set = models.ManyToManyField(BaseResolutionTable)
    bitrate_set = models.ManyToManyField(BaseBitrateTable)
    framerate_set = models.ManyToManyField(BaseFramerateTable)

    editor_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.model_name)

    def get_content(self):
        #todo:
        pass

    def get_model_name(self):
        return unicode(self.model_name)

    class Meta:
        ordering = ('id',)


class VideoSettingTable(models.Model):
    """
    设置表
    """
    mac_addr = models.CharField(max_length=16, unique=True)
    current_ip = models.IPAddressField()
    type_id = models.ForeignKey(BaseTypeTable)

    set_resolution = models.CharField(max_length=20)
    set_bitrate = models.IntegerField(max_length=10)
    set_framerate = models.CharField(max_length=20)
    #操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示
    operate_type = models.IntegerField(max_length=2, default=1)

    editor_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    status = models.IntegerField(max_length=1, default=0)

    def __unicode__(self):
        return unicode(self.mac_addr)

    def get_content(self):
        # todo:
        pass

    class Meta:
        ordering = ('id',)


class MissionInfoTable(models.Model):
    """
    任务简表
    """
    mission_id = models.CharField(max_length=20,unique=True)
    total_count = models.IntegerField(max_length=5)
    progress = models.IntegerField(max_length=5, default='0')

    remote_id = models.CharField(max_length=20, default='0')
    editor_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.mission_id)

    def get_content(self):
        # todo:
        pass

    class Meta:
        ordering = ('mission_id',)

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
    #操作类型，1：设置码流参数   2：设置码流参数并同步OSD显示
    operate_type = models.IntegerField(max_length=2, default=1)


    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    status = models.IntegerField(max_length=1, default=0)

    def __unicode__(self):
        return unicode(self.current_ip)

    def get_content(self):
        # todo:
        pass

    class Meta:
        ordering = ('mac_addr',)
