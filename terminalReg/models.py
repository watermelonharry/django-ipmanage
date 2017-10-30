# -*- coding: utf-8 -*-
from django.db import models
import time
import datetime

TERMINAL_BURN_TIME = 60


class TerminalModel(models.Model):
    """
    terminal registration
    """
    TERMINAL_STATUS_LIST = [
        (0, u'离线'),
        (1, u'空闲'),
        (2, u'繁忙'),
        (3, u'出错'),
    ]

    terminal_name = models.CharField(max_length=40, blank=True, unique=True)
    terminal_status = models.IntegerField(blank=True, null=True, choices=TERMINAL_STATUS_LIST)
    terminal_type = models.CharField(max_length=20, blank=True, null=True)

    user_name = models.CharField(max_length=30, blank=True)
    assigned_mission = models.CharField(max_length=20, blank=True, null=True)

    available_time = models.IntegerField(blank=True, null=True)

    ak = models.CharField(max_length=50, blank=True, null=True)
    terminal_addr = models.CharField(max_length=20, blank=True, null=True)
    terminal_port = models.IntegerField(blank=True, null=True)

    other_info = models.TextField(blank=True, null=True)

    version = models.CharField(max_length=20,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edit_time', 'id']

    def __unicode__(self):
        return self.terminal_name

    @classmethod
    def get_terminal_by_name(cls, terminal_name):
        try:
            terminal = cls.objects.get(terminal_name=terminal_name)
            return terminal
        except Exception as e:
            return None

    def is_online(self):
        """
        check the edit time to decide whether the terminal is online
        5 seconds burn time
        :return:
        """
        # todo: compare edit time with localtime
        record = self.edit_time

        try:
            live_time = self.available_time
        except Exception as e:
            live_time = TERMINAL_BURN_TIME

        now = datetime.datetime.now(tz=record.tzinfo)
        time_gap = now - record
        tall = abs(time_gap.days * 60 * 60 * 24 + time_gap.seconds)
        if tall < live_time:
            return True
        else:
            return False

    def update_data(self, **kwargs):
        user_name = kwargs.get('user_name', None)
        if user_name:
            self.user_name = user_name
            self.save()
        else:
            pass

    @classmethod
    def get_online_list(cls):
        """
        get online-terminal list
        """
        all_terminal = cls.objects.all()
        online_list = []
        for terminal in all_terminal:
            if terminal.is_online():
                online_list.append(terminal)
        return online_list

    @classmethod
    def has_terminal(cls, input_name):
        """
        :param input_name:
        :return:
        """
        try:
            terminal = cls.objects.get(terminal_name=input_name)
            return True
        except Exception as e:
            return False

    def get_other_info_html(self):
        """
        translate other info to html
        :return: html output
        """
        output_str = u""
        try:

            other_info_dict = eval(self.other_info)
            for key,val in other_info_dict.items():
                if key == "registered_module":
                    output_str += u"<p>模块: {0}</p>".format(u', '.join(val))
                else:
                    output_str += u"<p>{0}: {1}</p>".format(key, u', '.join(val))
        except Exception as e:
            pass
        finally:
            return output_str


class TerminalHistoryModel(models.Model):
    """
    record the mission excuting history
    """

    terminal_id = models.IntegerField(blank=True)
    mission_id = models.CharField(max_length=40, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.terminal_id + self.mission_id

    class Meta:
        ordering = ['id', 'create_time']


class TerminalWaitingMissionModel(models.Model):
    """
    newly created mission waiting to be fetched by terminals
    """
    mission_status_choice = [
        (1, u'待分配'),
        (2, u'已下发')
    ]
    terminal_name = models.CharField(max_length=40)
    mission_id = models.CharField(max_length=40)

    # module
    user_name = models.CharField(max_length=30, blank=True)
    mission_from = models.CharField(max_length=20)
    mission_url = models.CharField(max_length=40, blank=True, null=True)

    mission_status = models.IntegerField(choices=mission_status_choice, default=1)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.terminal_name + self.mission_id

    class Meta:
        ordering = ['id', 'create_time']

    def update_data(self, **kwargs):
        user_name = kwargs.get('user_name', None)
        if user_name:
            self.user_name = user_name
            self.save()
        else:
            pass

    @classmethod
    def delete_from_queue(cls, mission_id):
        """
        waiting mission deleter
        :param mission_id:
        :return:
        """
        try:
            cls.objects.get(mission_id=mission_id).delete()
            return True
        except Exception as e:
            return False

    @classmethod
    def get_mission_by_terminal_name(cls, terminal_name):
        """
        get waiting mission by input terminal_name
        :param terminal_name:
        :return:
        """
        try:
            single_mission = cls.objects.filter(terminal_name=terminal_name).filter(mission_status=1)[0]
            single_mission.mission_status = 2
            single_mission.save()
            return single_mission
        except Exception as e:
            return None
