"""
module to call api module
"""
try:
    import requests
    import re
    import threading
    import time

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
