# -*- coding: UTF-8 -*
"""
__VERSION__ = '2017.10.12'
__author__ = 'heyu'

description: uploader thread used in terminal
change list:
1. 2017.10.12, 新建文件
"""

try:
	import re
	import threading
	import time
	import json
	import random
	import Queue
	import logging
	import hashlib
	import random
	import os
	import requests
except Exception as e:
	print('[*] import error:' + e.message)
	raise e

"""
Globals here
"""

"""
log settings
"""
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(name)s-%(funcName)s-%(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("terminal.log")
file_handler.setFormatter(formatter)

# DispatcherThread
logger = logging.getLogger("UploaderThread")
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# RegisterThread
logger = logging.getLogger("UploadDataFormatter")
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger = logging.getLogger('uploaderapi-module')
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

"""
classes and functions here
"""

__instance_dict = {}


def get_Uploader(ak="", **kwargs):
	"""
	get uploader thread instance in singleton mode,
	the instances are indexed by ak,terminal name and other kwargs.
	:param ak:(str) input ak
	:param kwargs: other kwargs
	:return: an running instance of class "UploaderThread"
	"""
	key_str = "{0}".format(ak)
	for val in kwargs.itervalues():
		key_str += "{0}".format(val)

	key = generate_hash_id(str(key_str))
	logger.debug("searching UploaderThread with key:{0}".format(key))
	if __instance_dict.get(key, None):
		if __instance_dict[key].is_alive():
			logger.debug("existing UploaderThread instance with key:{0}, returning".format(key))
			return __instance_dict[key]
		else:
			logger.debug("dead UploaderThread instance with key:{0}, reinitializing".format(key))
			del __instance_dict[key]
	logger.debug("init UploaderThread with ak:{0}".format(ak))
	instance = UploaderThread(ak=ak, **kwargs)
	__instance_dict[key] = instance
	instance.start()
	return instance


def generate_hash_id(str_in=""):
	"""
	generate unique id based on given str
	:param str_in: given str/int/float
	:return: hash id(str), length is 16
	"""
	m = hashlib.md5()
	m.update("{0}".format(str_in))
	key = m.hexdigest()[:16]
	del m
	return key


def generate_hash_id_with_salt(str_in=str(time.time() * 1000)):
	"""
	generate unique id based on time(ms) or given str with random salt
	:param str_in: source string
	:return: hash id(str), length is 16
	"""
	salt = str(random.random())
	return generate_hash_id(str_in="{0}{1}".format(str_in, salt))


class UploadDataFormatter(object):
	def __init__(self, ak=None, terminal_name=None, offset=0, limit=10, **kwargs):
		self.logger = logging.getLogger('UploadDataFormatter')
		self._ak = ak
		self._terminal_name = terminal_name
		self._format_dict = {"ak": ak,
		                     "terminal_name": terminal_name,
		                     "offset": offset,
		                     "limit": limit,
		                     "data": {}}
		for key, val in kwargs.items():
			self._format_dict.update({key: val})
		self.logger.debug("init with param {0}".format(str(self)))

	def __str__(self):
		return u'ak:{0},terminal_name:{1}'.format(self._ak, self._terminal_name)

	def set_ak(self, ak=None):
		if not ak:
			self._ak = ak
			self._format_dict.update(ak=ak)

	def set_terminal_name(self, terminal_name=None):
		if not terminal_name:
			self._terminal_name = terminal_name
			self._format_dict.update(terminal_name=terminal_name)

	def get_format_post_data(self, data=None, **kwargs):
		self.logger.debug("format POST data {0}".format(data))
		temp_dict = {}
		temp_dict.update(self._format_dict)
		try:
			temp_dict.update({"data": data})
			for key, val in kwargs.items():
				temp_dict.update({key: val})
			self.logger.debug("formatting POST finish, data:{0}".format(temp_dict))
		except Exception as e:
			self.logger.error("formatting data {0}, {1}".format(data, e))
		finally:
			return temp_dict

	def get_format_get_data(self, offset=0, limit=10, **kwargs):
		self.logger.debug("format GET data {0}".format(kwargs))
		temp_dict = {}
		temp_dict.update(self._format_dict)
		try:
			temp_dict.update({"offset": offset, "limit": limit})
			for key, val in kwargs.items():
				temp_dict.update({key: val})
			self.logger.debug("formatting GET finish, data:{0}".format(temp_dict))
		except Exception as e:
			self.logger.error("formatting data {0}, {1}".format(kwargs, e))
		finally:
			return temp_dict


class UploaderThread(threading.Thread):
	def __init__(self, ak=None, **kwargs):
		super(UploaderThread, self).__init__()
		self.__wait_queue = Queue.Queue()
		self.__temp_wait_dict = {}
		self.ak = ak
		self.last_update_time = time.time()
		self.temp_file_path = "uploader.temp"
		self.__temp_file_handler = None
		self.upload_gap = 0.5
		self.RUN_FLAG = True
		self.TERMINATE_FLAG = False
		self.logger = logging.getLogger("UploaderThread")
		if not self.ak:
			self.logger.error("ERROR init uploader thread, no ak defined")
			raise ValueError("ERROR init uploader thread, no ak defined")
		self.logger.debug("uploader thread initiated.")
		self.read_temp_from_file()

	def __str__(self):
		return u"uploader thread {0} with temp file {1}".format(self.getName(), self.temp_file_path)

	def verify_upload_data(self, data=None):
		"""
		verify the data is in correct format
		:return:True/False
		"""
		check_list = ['dst_url', 'data', 'expected_reply', 'method']
		try:
			for check_point in check_list:
				if not data.get(check_point, None):
					raise ValueError("{0} is empty".format(check_point))
			return True
		except Exception as e:
			self.logger.error("data {0} failed verification with error-{1}, abandon this package.".format(data, e))
			return False

	def pack_data(self, data=None):
		"""
		pack data with uid
		:param data:
		:return: {uid: data}
		"""
		uid = generate_hash_id_with_salt()
		return {uid: data}

	def update_temp_to_file(self):
		"""
		export temp data to temp file
		:return: None/Exception
		"""
		try:
			with open(self.temp_file_path, 'w') as f:
				f.write(json.dumps(self.__temp_wait_dict))
		except Exception as e:
			self.logger.error("ERROR export data to temp file, {0}".format(e))

	def __update_to_instance(self, data):
		self.logger.debug("update data {0} to mission queue".format(data))
		self.__wait_queue.put(data)
		self.__temp_wait_dict.update(data)

	def read_temp_from_file(self):
		"""
		load unfinished data from temp file
		:return:None/Exception
		"""
		try:
			self.logger.debug("load temp data from file {0}".format(self.temp_file_path))
			with open(self.temp_file_path, 'r') as f:
				temp_data = json.loads(f.readline())
				for key, val in temp_data.items():
					self.__update_to_instance({key: val})
			self.update_temp_to_file()
			self.logger.debug("load from temp finish.")
		except Exception as e:
			self.logger.error("ERROR load temp data from file, {0}".format(e))

	def push_to_queue(self, data=None):
		"""
		push date to waiting queue
		:param data: dict or list data, eg. {"target_url":xxx, "data":xxxx, "expected_status":200, call_back}
		:return:True/ exception
		"""
		if isinstance(data, dict):
			formatted_data = self.pack_data(data=data)
			self.add_single_data_to_queue(formatted_data)

		elif isinstance(data, list):
			for single_data in data:
				formatted_data = self.pack_data(data=single_data)
				self.add_single_data_to_queue(formatted_data)
		else:
			self.logger.error("unsupported data type-{0}".format(type(data)))

	def add_single_data_to_queue(self, data=None):
		try:
			self.__update_to_instance(data=data)
			self.update_temp_to_file()
			self.logger.debug("data {0} push to waiting queue.".format(data))
		except Exception as e:
			self.logger.error("ERROR add data {0} to queue, {1}".format(data, e))

	def remove_single_data_from_temp(self, data={}, uid=None):
		try:
			temp_uid = data.get('uid', None)
			if uid is not None:
				temp_uid = uid
			self.__temp_wait_dict.pop(temp_uid)
			self.update_temp_to_file()
			self.logger.debug("remove data {0} from temp".format(temp_uid))
		except Exception as e:
			self.logger.error("ERROR remove data {0} from temp".format(temp_uid))

	def upload_data_to_server(self):
		self.wait_enough()

		formatted_data = self.__wait_queue.get()
		uid, data = formatted_data.popitem()
		# data:
		# {"target_url": xxx, "data": xxxx, "expected_status": 200, call_back}
		if not self.verify_upload_data(data):
			self.remove_single_data_from_temp(uid=uid)
			return False

		try:
			target_url = data['dst_url']
			temp_data = {}
			temp_data.update(data['data'])
			# temp_data.update({"ak": self.ak})
			upload_data = temp_data
			expected_status_code = int(data['expected_reply'])
			request_method = data['method'].lower()
			call_back_func = data.get("call_back", None)

			if request_method == "put":
				reply = requests.put(url=target_url, data=json.dumps(upload_data))
			elif request_method == "post":
				reply = requests.api.post(url=target_url, json=json.dumps(upload_data), timeout=10)
			elif request_method == "get":
				reply = requests.get(url=target_url, params=upload_data)
			elif request_method == "delete":
				reply = requests.delete(url=target_url, data=json.dumps(upload_data))

			if reply.status_code == expected_status_code:
				self.logger.debug("upload data {0}:{1} finish.".format(uid, upload_data))
				self.remove_single_data_from_temp(uid=uid)
				if call_back_func:
					try:
						call_back_data = reply.json()
						call_back_func(data=call_back_data)
					except Exception as e:
						self.logger.error(
							"ERROR:call func {0} with data {1}, {2}".format(call_back_func, call_back_data, e))
			else:
				raise ValueError("ERROR uploading data {0}, status code {1}".format(upload_data, reply.status_code))
		except Exception as e:
			self.logger.error("{0}".format(e))
			self.add_single_data_to_queue(data={uid: data})

	def wait_enough(self):
		"""
		assure the upload frequency is reasonable
		:return: None
		"""
		time_now = time.time()
		while time_now - self.last_update_time < self.upload_gap:
			time.sleep(self.upload_gap / 3)
			time_now = time.time()
		self.last_update_time = time_now

	def run(self):
		while not self.TERMINATE_FLAG:
			# keep running

			while self.RUN_FLAG:
				# keep uploading
				self.upload_data_to_server()

			self.logger.info("uploader thread has been halted for 5 seconds. uploading PAUSED.")
			time.sleep(5)

		self.logger.info("terminate uploader thread.")

	def terminate_thread(self):
		self.logger.debug("set terminated flag to True, thread terminated")
		self.RUN_FLAG = False
		self.TERMINATE_FLAG = True
		self.push_to_queue(data={'terminate_thread': True})

	def halt_thread(self):
		self.logger.debug("set RUN flag to False, halt uploading")
		self.RUN_FLAG = False

	def restart_thread(self):
		self.logger.debug("set RUN flag to True, restart uploading")
		self.RUN_FLAG = True


if __name__ == '__main__':
	"""usage"""
	"""
	uploader = UploaderThread(ak="xxxxxxx")
	uploader.start()
	
	post_data = {'dst_url':"http://127.0.0.1:8000/iottest/api/test/", 'data':{"v1":"nanana","v2":"bobbo"}, 'expected_reply':200, 'method':"POST"}
	uploader.push_to_queue(data=post_data)
	
	"""
	"""
	f = UploadDataFormatter(ak="12341123", terminal_name='test_terminal')
	content= f.get_format_post_data(data={"v1":1234,"v2":5678})
	"""
