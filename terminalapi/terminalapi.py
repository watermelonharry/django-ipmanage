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
REQUEST_COUNT = 5
TIME_OUT = 2.0
REGISTER_PATH = 'terminal/api/register/'

"""
class here
"""

request_pool = threading.Semaphore(REQUEST_COUNT)


class RegisterThread(threading.Thread):
    """
    register thread, request the URL
    """

    def __init__(self, interval=5, **kwargs):
        super(RegisterThread, self).__init__()
        self.interval_time = interval

        self.terminal_name = kwargs.get('terminal_name', 'unknown')
        self.root_url = kwargs.get('url', 'http://127.0.0.1:8000/')
        self.ak = kwargs.get('ak', 'no_ak')

        self.reg_url = self.root_url + '/' + REGISTER_PATH
        self.RUN_FLAG = True

        self.info_dict = {
            'terminal_name': self.terminal_name,
            'ak': self.ak,
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
            # todo: post and get result
            pass

    def post(self):
        """
        post data to register_url
        :return:
        """
        try:
            reply = requests.api.post(self.reg_url, json=self.info_dict, timeout=TIME_OUT)
            if reply.status_code == 200:
                re_dict = reply.json()
                self.CONNECTION_STATUS = 1
                return re_dict
            else:
                raise requests.exceptions.ConnectionError

        except Exception as e:
            ##connect error
            self.CONNECTION_STATUS = 2
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
        return self.CONNECTION_STATUS

    def stop(self):
        """
        stop the register thread
        :return: None
        """

    def set_params(self, **kwargs):
        """
        change the post params in thread
        :param kwargs: params dict
        :return: None
        """
        # todo: manager Thread
