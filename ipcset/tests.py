# -*- coding: utf-8 -*-

from django.test import TestCase, Client

# Create your tests here.

from models import *


class IotDeviceModelTest(TestCase):
	@classmethod
	def setUpClass(cls):
		new_device = IotDeviceTable(device_name='test_device',
		                            device_type='h265',
		                            device_addr='192.168.1.20',
		                            device_username='admin',
		                            device_ov_password='101910',
		                            device_web_password='101910',
		                            editor_name='tester')
		new_device.save()

		new_device_2 = IotDeviceTable(device_name='test_device_2',
		                              device_type='h264',
		                              device_addr='192.168.1.120',
		                              device_username='admin',
		                              device_ov_password='101910',
		                              device_web_password='101910',
		                              editor_name='tester')
		new_device_2.save()

	def test_get_sut_list_no_ordering(self):
		sut_list = IotDeviceTable.get_sut_list()
		self.assertEqual(len(sut_list), 2)
		self.assertEqual(sut_list[0].device_addr, '192.168.1.20')
		self.assertEqual(sut_list[1].device_addr, '192.168.1.120')

	def test_get_sut_list_ordered_by_ip(self):
		sut_list = IotDeviceTable.get_sut_list(ordering='ip')
		self.assertEqual(len(sut_list), 2)
		self.assertEqual(sut_list[0].device_addr, '192.168.1.20')
		self.assertEqual(sut_list[1].device_addr, '192.168.1.120')

	def test_get_sut_list_ordered_by_ip_reversed(self):
		sut_list = IotDeviceTable.get_sut_list(ordering='-ip')
		self.assertEqual(len(sut_list), 2)
		self.assertEqual(sut_list[1].device_addr, '192.168.1.20')
		self.assertEqual(sut_list[0].device_addr, '192.168.1.120')

	def test_get_sut_list_ordered_by_error_key(self):
		sut_list = IotDeviceTable.get_sut_list(ordering='no_exisit')
		self.assertEqual(len(sut_list), 2)

	def test_get_sut_ids(self):
		sut_ids = IotDeviceTable.get_sut_ids()
		self.assertEqual(len(sut_ids),2)
		self.assertTrue(1 in sut_ids)
		self.assertTrue(2 in sut_ids)

class MissionTableModelTest(TestCase):
	@classmethod
	def setUpClass(cls):
		pass