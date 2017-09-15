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
    import Queue
    import logging

except Exception as e:
    print('[*] import error:' + e.message)
    raise e

"""
Globals here
"""
THREAD_COUNT = 5
TIME_OUT = 2.0
ROOT_PATH = 'http://127.0.0.1:8000'
REGISTER_PATH = '/terminal/api/register/'
REGISTER_INTERVAL = 30

mission_queue = Queue.Queue()
request_pool = threading.Semaphore(THREAD_COUNT)


class CONNECTION_STATUS(object):
    OFFLINE = 0
    IDLE = 1
    BUSY = 2
    ERROR = 3

"""
log settings
"""
formatter = logging.Formatter("%(asctime)s- %(levelname)s- %(name)s- %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler =  logging.FileHandler("terminal.log")
file_handler.setFormatter(formatter)

# DispatcherThread
logger = logging.getLogger("DispatcherThread")
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# RegisterThread
logger = logging.getLogger("RegisterThread")
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# ReceiverThread
logger = logging.getLogger("ReceiverThread")
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

"""
classes here
"""


class DispatcherThread(threading.Thread):
    def __init__(self, **kwargs):
        super(DispatcherThread, self).__init__()
        self.__dispatch_dict = {}
        self.__mission_queue = Queue.Queue()
        self.__RUN_FLAG = True
        self.__register_lock = threading.Lock()
        self.__set_status_func = None
        self.__THREAD_RUN_LOCK = threading.Lock()
        self.__api_root_url = kwargs.get('api_root_url', 'http://127.0.0.1:8000')
        self.logger = logging.getLogger("DispatcherThread")

    def say(self, words):
        print('[*] {0}'.format(str(words)))
        self.logger.info('{0}'.format(str(words)))

    def link_func_set_terminal_status(self, func):
        self.__set_status_func = func

    def set_terminal_status(self, status):
        self.__set_status_func(status)

    @property
    def is_running(self):
        return self.__RUN_FLAG

    def terminate(self):
        self.say('thread terminated.')
        self.__RUN_FLAG = False

    @property
    def dispatch_dict(self):
        return self.__dispatch_dict

    @property
    def mission_queue(self):
        return self.__mission_queue

    def get_mission_blocked(self):
        """
        block the threading until a new mission is assigned
        """
        self.say('getting mission.')
        return self.__mission_queue.get()

    def append_to_mission_queue(self, mission):
        """
        put new mission to mission_queue
        :param mission(dict): {'module':XXXX, 'data':{....}}
        :return:
        """
        self.say('new mission appended.')
        self.say('new mission is {0}.'.format(str(mission)))
        self.__mission_queue.put(mission)

    # @dispatch_dict.setter
    def __set_dispatch_dict(self, module, callfunc):
        self.__register_lock.acquire()
        try:
            self.__dispatch_dict[module] = callfunc

            self.__register_lock.release()
            return True
        except Exception as e:
            self.__register_lock.release()
            return False

    def register_module(self, module, callback):
        """
        add module - callback function relations to dispatch dict
        :param module: module name
        :param callback: callback function
        :return:
        """
        self.say('new module registering:{0}.'.format(module))
        return self.__set_dispatch_dict(module, callback)

    def dispatch(self, module, data, *args, **kwargs):
        """
        dispatch mission with module name and params
        :param module:
        :param kwargs:
        :return:
        """
        self.say('dispatch mission.')
        if self.dispatch_dict.has_key(module):
            self.set_terminal_status(CONNECTION_STATUS.BUSY)

            self.__register_lock.acquire()

            try:
                target_func = self.dispatch_dict.get(module, None)(data=data,
                                                                   api_root_url=self.__api_root_url,
                                                                   *args,
                                                                   **kwargs)  # todo:, *args, **kwargs
            except Exception as e:
                print('[*]error in dispatch:{0}'.format(e.message))

            self.__register_lock.release()

            try:
                if isinstance(target_func, threading.Thread):
                    # lock and run single thread
                    # self.__THREAD_RUN_LOCK.acquire()
                    print("[*] start {0} thread.".format(module))
                    target_func.start()
                    target_func.join()
                    print("[*] end {0} thread.".format(module))

                    # self.__THREAD_RUN_LOCK.release()
                else:
                    self.set_terminal_status(CONNECTION_STATUS.IDLE)
                    return target_func
            except Exception as e:
                print('[*]error in call target_func:{0}'.format(e.message))

            self.set_terminal_status(CONNECTION_STATUS.IDLE)
        else:
            pass

    def run(self):
        """
        1. get mission from queue
        2. dispatch mission and run
        """
        self.say('dispatcher thread running.')
        while self.is_running:

            try:
                self.say('waiting for mission')
                new_mission = self.get_mission_blocked()
                self.say('new mission get: {0}'.format(str(new_mission)))

                ret = self.dispatch(module=new_mission.get('module'), data=new_mission.get('data'))
                self.say('dispatch result is {0}'.format(ret))
                self.say('dispatch finished')
                # time.sleep(5)
            except Exception as e:
                self.say('error in DispatcherThread:{0}'.format(e))

        self.say('dispatch thread end')


class RegisterThread(threading.Thread):
    """
    register thread, request the URL
    """

    def __init__(self, interval=REGISTER_INTERVAL, api_root_url=ROOT_PATH, register_path=REGISTER_PATH, **kwargs):
        super(RegisterThread, self).__init__()
        ##dispatch dict, module and its process thread
        self.interval_time = interval
        self.api_root_url = api_root_url
        self.register_path = register_path
        self.ak = kwargs.get('ak', 'no_ak')
        self.terminal_name = kwargs.get('terminal_name', 'not set')
        self.reg_url = self.api_root_url + self.register_path

        self.RUN_FLAG = True
        self.CONNECTION_STATUS = CONNECTION_STATUS.OFFLINE
        self.logger = logging.getLogger("RegisterThread")

        self.info_dict = {
            'terminal_name': self.terminal_name,
            'ak': self.ak,
            'terminal_status': CONNECTION_STATUS.IDLE,
            'assigned_mission': None,
            'register_url': self.reg_url,
            'available_time': self.interval_time / 2,
            'terminal_addr': None,
            'terminal_port': None,
            'other_info': {'registered_module': []},
        }

        self.LOCK = threading.Lock()  # r/w lock for variants

        """
        0: no connection
        1: connected
        2: error in connecting
        """
        self.CONNECTION_STATUS = 0

        ##init other Thread
        try:
            self.__dispath_thread = DispatcherThread(api_root_url=self.api_root_url)
            self.__dispath_thread.link_func_set_terminal_status(self.set_terminal_status)
            self.__dispath_thread.start()

            MyTCPHandler.register_handle_func(self.__dispath_thread.append_to_mission_queue)
            self.__receiver_thread = ReceiverThread()
            self.info_dict.update(self.__receiver_thread.get_info_dict())
            MyTCPHandler.update_info_dict(self.info_dict)

        except Exception as e:
            self.RUN_FLAG = False
            self.say('[*] init sub thread error:{0}, quit Register Thread'.format(str(e)))

        self.say('[*] init register thread success:{0}.'.format(str(self.get_info_dict())))


    def say(self, words):
        self.say('[*] {0}'.format(str(words)))
        self.logger.info('{0}'.format(str(words)))

    def update_other_info(self, **kwargs):
        target = self.info_dict.get('other_info', [])
        try:
            for key, val in kwargs.items():
                if target.has_key(key):
                    target[key].append(val)
                else:
                    target.update({key: [val]})
                self.say('[*] {0}:{1} info updated.'.format(str(key), str(val)))
        except Exception as e:
            self.say('[*] ERROR: {0}:{1} info updating.'.format(str(key), str(val)))

    def register_module(self, module, callback):
        self.update_other_info(registered_module=module)
        return self.__dispath_thread.register_module(module, callback)

    def get_info_dict(self):
        return self.info_dict

    def set_terminal_status(self, status):
        self.say('[*] set terminal status {0}.'.format(status))
        self.info_dict['terminal_status'] = status

    def run(self):
        """
        post on time
        """
        while self.RUN_FLAG:
            reply_dict = self.post()
            if reply_dict is not None:
                self.dispatch_mission(self.extract_mission_dict(reply_dict))

            # todo:post and get result

            time.sleep(self.interval_time)

    def extract_mission_dict(self, reply_dict):
        """
        extract mission dict in dispatcher's pattern
        :param reply_dict: reply dict from server
        :return: mission_dict, eg. {'module':xxxx, 'data':{....params...}}
        """
        # todo:
        try:
            mission_data = reply_dict.get('data', {})
            mission_dict = {'module': mission_data.get('mission_from', 'unknown'),
                            'data': mission_data}
            return mission_dict
        except Exception as e:
            return {'module': 'unknown'}

    def dispatch_mission(self, mission_dict):
        """
        deliver the mission dict to dispatch thread and run
        :param mission_dict: mission_info_dict, eg: {'module':xxx, 'data':{....}}
        :return:
        """
        try:
            if mission_dict.get('data', {}).get('mission_id', "") != "":
                self.__dispath_thread.append_to_mission_queue(mission_dict)
            else:
                self.say("[*] mission id is empty, skip dispatch.")
        except Exception as e:
            pass

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

    def post(self, info_dict=None, post_url=None):
        """
        post data to register_url
        :return:
        """
        if info_dict is None:
            info_dict = self.info_dict
        if post_url is None:
            post_url = self.reg_url

        try:
            reply = requests.api.post(url=post_url, json=info_dict, timeout=TIME_OUT)
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

    def get(self, info_dict=None, post_url=None):
        """
        get status
        :return:
        """
        if info_dict is None:
            info_dict = self.info_dict
        if post_url is None:
            post_url = self.reg_url

        try:
            reply = requests.api.get(url=post_url, json=info_dict, timeout=TIME_OUT)
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
        self.logger = logging.getLogger("ReceiverThread")
        if self.__assign_port() is False:
            self.say('[*] receiver thread init failed, quit Receiver Thread.')
            raise AttributeError('receiver thread init failed, quit Receiver Thread.')

        else:
            self.say('[*] receiver thread init success with port: %s' % str(self.port))
            self.start()

    def say(self, words):
        self.say('[*] {0}'.format(str(words)))
        self.logger.info('{0}'.format(str(words)))

    def run(self):
        self.say('[*] start receive server.')
        self.server.serve_forever()

    def __start_tcp_server(self, host, port):
        try:
            self.server = socketserver.TCPServer((host, port), MyTCPHandler)
            return True
        except Exception as e:
            self.say(e.message)
            return False

    def __assign_port(self):
        retry_count = 5
        while retry_count > 0:
            self.port = random.randint(20000, 60000)
            if self.__start_tcp_server('0.0.0.0', self.port):
                return True
            else:
                retry_count -= 1
        return False

    def get_info_dict(self):
        """
        get the thread info dict
        :return: {"port":12313, ...}
        """
        info_dict = {"terminal_port": self.port}
        return info_dict


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    index_content = '''HTTP/1.x 200 ok\r\nContent-Type: application/json\r\n\r\n'''
    option_content = """HTTP/1.x 200 ok\r\nAccess-Control-Allow-Methods: POST\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Headers: accept, content-type\r\nContent-Type: application/json\r\n\r\n"""

    @classmethod
    def update_info_dict(cls, info_dict):
        if hasattr(cls, 'info_dict'):
            print('[*] Handler class already has info_dict attr, updating.')
            cls.info_dict.update(info_dict)
        else:
            print('[*] Handler class attr info_dict add success.')
            setattr(cls, 'info_dict', info_dict)

    def handle(self):
        # self.request is the TCP socket connected to the client
        time.sleep(0.1)
        request = self.request.recv(4096)
        # print("[*] get: \n{0}".format(request))
        method = request.split(' ')[0]
        src = request.split(' ')[1]
        if src != '/':
            return

        content = self.option_content

        # deal wiht GET method
        if method == 'GET':
            content += json.dumps({'error': 'none', 'data': {'a': 1, 'b': 2}})

        # deal with POST method
        elif method == 'POST':
            form = request.split('\r\n')
            entry_json = form[-1]  # main content of the request
            in_dict = json.loads(entry_json)
            if hasattr(self, 'handle_func'):
                print "[*] entering handle_func"

                self.handle_func(in_dict)

            else:
                print "[*] has no handle_func"
            re_dict = {}
            re_dict.update(self.info_dict)
            re_dict.update(in_dict)

            content += json.dumps({'error': 'none', 'data': re_dict})
        ######
        # More operations, such as put the form into database
        # ...
        ######
        elif method == 'OPTIONS':
            content = self.option_content
        else:
            pass

        # print "[*] {} wrote:".format(self.client_address[0])
        # print "[*] send back: {}".format(content)

        # just send back the same data, but upper-cased
        self.request.sendall(content)

    @classmethod
    def register_handle_func(cls, func):
        if hasattr(cls, 'handle_func'):
            print "[*] already has a handle_func, replaced"
            setattr(cls, ' handle_func', func)
        else:
            setattr(cls, 'handle_func', func)
            print "[*] handle_func registered"


def printer(x):
    print('[*] in printer func:{0}'.format(str(x)))


def summer(x, y):
    print('[*] in sum func: {0}'.format(str(x + y)))


class TestThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(TestThread, self).__init__()
        self.kdict = {}
        for key, val in kwargs.items():
            setattr(self, key, val)
            self.kdict[key] = val

    def run(self):
        for key, val in self.kdict.items():
            print("  [*] from {0}--{1}: {2} -- {3}".format(self.__class__, self.kdict['mission_id'], key, val))
            time.sleep(4)


if __name__ == '__main__':
    k = RegisterThread(ak='28e444bbe8d17bba573e', terminal_name='regi_terminal_35')
    k.register_module(module='print', callback=printer)
    k.register_module(module='sum', callback=summer)
    k.register_module(module='ipcset', callback=TestThread)
    k.start()
    k.join()

    """
    for test: send {"module":"sum", "data":{"x":20,"y":30}} to localhost:port
    for test: send {"module":"print", "data":{"x":20}} to localhost:port
    """
