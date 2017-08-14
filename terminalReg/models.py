# -*- coding: utf-8 -*-
from django.db import models
import time
import datetime

TERMINAL_BURN_TIME = 5


class TerminalModel(models.Model):
	"""
	terminal registration
	"""
	TERMINAL_STATUS_LIST = [
		(1, u'空闲'),
		(2, u'繁忙'),
	]

	terminal_name = models.CharField(max_length=40, blank=True, unique=True)
	terminal_status = models.IntegerField(blank=True, null=True)
	terminal_type = models.CharField(max_length=20, blank=True, null=True)

	available_time = models.IntegerField(blank=True, null=True)

	ak = models.CharField(max_length=50, blank=True, null=True)
	terminal_addr = models.CharField(max_length=20, blank=True, null=True)
	terminal_port = models.IntegerField(blank=True, null=True)

	other_info = models.TextField(blank=True, null=True)

	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-edit_time', 'id']

	def __unicode__(self):
		return self.terminal_name

	def is_online(self):
		"""
		check the edit time to decide whether the terminal is online
		5 seconds burn time
		:return:
		"""
		# todo: compare edit time with localtime
		record = self.edit_time
		now = datetime.datetime.now(tz=record.tzinfo)
		time_gap = now - record
		if time_gap.total_seconds() < TERMINAL_BURN_TIME:
			return True
		else:
			return False

	@classmethod
	def get_online_list(cls):
		"""
		get online-terminal list
		"""
		all_terminal = cls.objects.all()
		online_list =[]
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
	mission_from = models.CharField(max_length=20)
	mission_url = models.CharField(max_length=40, blank=True, null=True)

	mission_status = models.IntegerField(choices=mission_status_choice, default=1)

	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.terminal_name + self.mission_id

	class Meta:
		ordering = ['id', 'create_time']
