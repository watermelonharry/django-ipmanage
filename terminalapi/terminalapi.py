"""
module to call api module
"""
try:
	import requests
	import re
	import threading
	import time
	import json
	import SocketServer as socketserver
	import random

except Exception as e:
	print('[*] import error:' + e.message)
	raise e

"""
Globals here
"""
THREAD_COUNT = 5
TIME_OUT = 2.0
REGISTER_PATH = 'terminal/api/register/'

"""
class here
"""

request_pool = threading.Semaphore(THREAD_COUNT)


class CONNECTION_STATUS(object):
	OFFLINE = 0
	IDLE = 1
	BUSY = 2
	ERROR = 3


class RegisterThread(threading.Thread):
	"""
	register thread, request the URL
	"""

	def __init__(self, interval=5, **kwargs):
		super(RegisterThread, self).__init__()
		##dispatch dict, module and its process thread
		self.__dispatch = {}

		self.interval_time = interval

		self.terminal_name = kwargs.get('terminal_name', 'unknown')
		self.root_url = kwargs.get('url', 'http://127.0.0.1:8000/')
		self.ak = kwargs.get('ak', 'no_ak')

		self.reg_url = self.root_url + '/' + REGISTER_PATH
		self.RUN_FLAG = True
		self.CONNECTION_STATUS = CONNECTION_STATUS.OFFLINE

		self.info_dict = {
			'terminal_name': self.terminal_name,
			'ak': self.ak,
			'terminal_status': CONNECTION_STATUS.IDLE,
			'assigned_mission': None
		}

		self.LOCK = threading.Lock()

		"""
		0: no connection
		1: connected
		2: error in connecting
		"""
		self.CONNECTION_STATUS = 0

	def run(self):
		"""
		post on time
		"""
		while self.RUN_FLAG:
			assign_info = self.post()
			if assign_info is not None:
				self.dispatch_mission()

			# todo:post and get result
			fields = ('id', 'terminal_name', 'mission_id', 'mission_from', 'mission_url', 'mission_status', 'edit_time')

			time.sleep(self.interval_time)

	@property
	def dispatch_dict(self):
		return self.__dispatch

	@dispatch_dict.setter
	def __dispatch_dict(self, module, callback):
		self.__dispatch[module] = callback

	def register_module(self, module=None, callback=None):
		"""
		add module and its process threads to dispatch dict
		:return:
		"""
		if isinstance(module, str):
			self.__dispatch_dict(module=module, callback=callback)
		else:
			raise ValueError('module name can not be empty')

	def dispatch_mission(self):
		"""
		dispatch the mission according to the returning info
		:return:
		"""

	def set_status(self, status):
		"""
		set connection status
		:param status:
		:return:
		"""
		self.LOCK.acquire()
		self.CONNECTION_STATUS = status
		self.info_dict['terminal_status'] = status
		self.LOCK.release()

	def post(self):
		"""
		post data to register_url
		:return:
		"""
		try:
			reply = requests.api.post(self.reg_url, json=self.info_dict, timeout=TIME_OUT)
			if reply.status_code == 200:
				re_dict = reply.json()
				self.set_status(CONNECTION_STATUS.IDLE)
				return re_dict
			else:
				raise requests.exceptions.ConnectionError

		except Exception as e:
			##connect error
			self.set_status(CONNECTION_STATUS.ERROR)
			return None

	def get(self):
		"""
		get status
		:return:
		"""
		pass

	def get_connect_status(self):
		"""
		check if the connection is established
		:return: True/False
		"""
		self.LOCK.acquire()
		status = self.CONNECTION_STATUS
		self.LOCK.release()
		return status

	def stop(self):
		"""
		stop the register thread
		:return: None
		"""
		self.RUN_FLAG = False

	def set_params(self, **kwargs):
		"""
		change the post params in thread
		:param kwargs: params dict
		:return: None
		"""
		# todo: manager Thread
		pass


class ReceiverThread(threading.Thread):
	def __init__(self):
		super(ReceiverThread, self).__init__()
		if self.__assign_port() is False:
			print('[*] receiver thread init failed')
		else:
			print('[*] receiver thread init success with port: %s' %str(self.port))
			self.start()

	def run(self):
		print('[*] start receive server.')
		self.server.serve_forever()

	def __start_tcp_server(self, host, port):
		try:
			self.server = socketserver.TCPServer((host, port), MyTCPHandler)
			return True
		except Exception as e:
			print(e.message)
			return False

	def __assign_port(self):
		retry_count = 5
		while retry_count > 0:
			self.port = random.randint(20000,60000)
			if self.__start_tcp_server('0.0.0.0', self.port):
				return True
			else:
				retry_count -=1
		return False


class MyTCPHandler(socketserver.BaseRequestHandler):
	"""
	The request handler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""
	index_content = '''HTTP/1.x 200 ok\r\nContent-Type: application/json\r\n\r\n'''

	def handle(self):
		# self.request is the TCP socket connected to the client
		request = self.request.recv(2048)
		method = request.split(' ')[0]
		src = request.split(' ')[1]
		if src != '/':
			return

		content = self.index_content

		print 'Request is:\n', request

		# deal wiht GET method
		if method == 'GET':
			content += json.dumps({'error': 'none', 'data': {'a': 1, 'b': 2}})

		# deal with POST method
		elif method == 'POST':
			form = request.split('\r\n')
			entry_json = form[-1]  # main content of the request
			in_dict = json.loads(entry_json)
			re_dict = {'a': 1, 'b': 2}
			re_dict.update(in_dict)

			content += json.dumps({'error': 'none', 'data': re_dict})
		######
		# More operations, such as put the form into database
		# ...
		######
		else:
			pass

		print "[*] {} wrote:".format(self.client_address[0])
		print "[*] send back: {}".format(content)

		# just send back the same data, but upper-cased
		self.request.sendall(content)

if __name__=='__main__':
	k = ReceiverThread()