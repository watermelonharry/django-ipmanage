# -*- coding: utf-8 -*-

from django.db import models


# Create your models here.
class IotDeviceTable(models.Model):
	TYPE_CHOICE = (('h264', u'H264'), ('h265', u'H265'))

	device_name = models.CharField(max_length=50)
	device_type = models.CharField(max_length=10, choices=TYPE_CHOICE, blank=True)

	device_addr = models.IPAddressField(blank=True)
	device_username = models.CharField(max_length=40, blank=True)
	device_ov_password = models.CharField(max_length=40, null=True, blank=True)
	device_web_password = models.CharField(max_length=40, null=True, blank=True)
	device_software_version = models.CharField(max_length=40, null=True, blank=True)

	other_info = models.TextField(blank=True, null=True)
	editor_name = models.CharField(max_length=20, blank=True)
	username = models.CharField(max_length=20, blank=True, null=True)

	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u"{0}-{1}".format(self.device_name, self.device_type)

	class Meta:
		ordering = ("device_addr",)
		unique_together = (("device_addr", "username"),)

	@classmethod
	def get_sut_ids(cls):
		id_list = []
		try:
			suts = cls.objects.all()
			for sut in suts:
				id_list.append(sut.id)
		except Exception as e:
			pass
		finally:
			id_list.sort()
			return id_list


class MissionTable(models.Model):
	TYPE_CHOICE = (('h264', u'H264'), ('h265', u'H265'))
	STATUS_CHOICE = ((0, u'等待'), (1, u'执行中'), (2, u'完成'), (3, u'终止'), (4, u'异常'))

	# mission_id = models.CharField(max_length=40, unique=True, blank=True)

	dut_name = models.CharField(max_length=20, blank=True)
	dut_version = models.CharField(max_length=40, blank=True)
	dut_addr = models.IPAddressField(blank=True)
	dut_type = models.CharField(max_length=10, choices=TYPE_CHOICE, blank=True)

	dut_username = models.CharField(max_length=40, blank=True)
	dut_password = models.CharField(max_length=40, null=True, blank=True)

	dut_cmp_lock = models.IntegerField(max_length=5, blank=True, null=True)
	other_info = models.TextField(blank=True, null=True)
	mission_status = models.IntegerField(max_length=5, choices=STATUS_CHOICE, blank=True)
	mission_progress = models.IntegerField(max_length=5, blank=True, null=True)
	mission_total= models.IntegerField(max_length=5,blank=True,null=True)
	sut_ids = models.ManyToManyField(IotDeviceTable,blank=True, null=True)

	terminal_name = models.CharField(max_length=40,blank=True)
	username = models.CharField(max_length=20, blank=True, null=True)
	editor_name = models.CharField(max_length=20, blank=True)
	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u"{0}".format(self.id)

	class Meta:
		ordering = ("-create_time",)


class MissionDetailTable(models.Model):
	RESULT_CHOICE = (
		("PASS", "PASS"),
		("FAIL", "FAIL"),
		("N/T", "N/T"),
		("REF", "REF")
	)

	mission_id = models.ForeignKey(MissionTable, blank=True, null=True, on_delete=models.CASCADE)
	# foreign key to iot device table
	iot_device_id = models.ForeignKey(IotDeviceTable, blank=True, null=True, on_delete=models.CASCADE)

	can_discover = models.CharField(max_length=10, choices=RESULT_CHOICE, blank=True)
	# discover_comment = models.TextField(null=True, blank=True)

	can_add = models.CharField(max_length=10, choices=RESULT_CHOICE, blank=True)
	# add_comment = models.TextField(null=True, blank=True)

	can_preview = models.CharField(max_length=10, choices=RESULT_CHOICE, blank=True)
	# preview_comment = models.TextField(null=True, blank=True)

	can_calculate = models.CharField(max_length=10, choices=RESULT_CHOICE, blank=True)
	# calculate_comment = models.TextField(null=True, blank=True)

	can_delete = models.CharField(max_length=10, choices=RESULT_CHOICE, blank=True)
	# delete_comment = models.TextField(null=True, blank=True)
	comment = models.TextField(blank=True,null=True)

	other_info = models.TextField(blank=True, null=True)
	dut_cmp_lock = models.IntegerField(max_length=5, blank=True, null=True)

	username = models.CharField(max_length=20, blank=True, null=True)

	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u"{0}-{1}".format(self.mission_id.id, self.iot_device_id.device_name)

	class Meta:
		ordering = ("id",)
		unique_together = (("mission_id", "iot_device_id"), ("id",),)

	@classmethod
	def get_details_by_mission_id(cls, m_id):
		try:
			detail_list = cls.objects.filter(mission_id=m_id)
		except Exception as e:
			detail_list = []
		finally:
			return detail_list
