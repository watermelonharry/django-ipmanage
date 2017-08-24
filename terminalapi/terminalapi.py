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
mission_queue = Queue.Queue()
request_pool = threading.Semaphore(THREAD_COUNT)


class CONNECTION_STATUS(object):
    OFFLINE = 0
    IDLE = 1
    BUSY = 2
    ERROR = 3


class DispatcherThread(threading.Thread):
    def __init__(self):
        super(DispatcherThread,self).__init__()
        self.__dispatch_dict = {}
        self.__mission_queue = Queue.Queue()
        self.__RUN_FLAG = True
        self.__register_lock =  threading.Lock()

    def say(self, words):
        print('[*] {0}'.format(str(words)))

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

    def dispatch(self, module, *args, **kwargs):
        """
        dispatch mission with module name and params
        :param module:
        :param kwargs:
        :return:
        """
        self.say('dispatch mission.')
        if self.dispatch_dict.has_key(module):
            self.__register_lock.acquire()
            target_func =  self.dispatch_dict.get(module)(*args, **kwargs)
            self.__register_lock.release()
            if isinstance(target_func, threading.Thread):
                target_func.start()
                target_func.join()
            else:
                return target_func
        else:
            pass

    def run(self):
        """
        1. get mission from queue
        2. dispatch mission and run
        """
        self.say('dispatcher thread running.')
        while self.is_running:
            self.say('waiting for mission')
            new_mission = self.get_mission_blocked()
            self.say('new mission get: {0}'.format(str(new_mission)))

            ret = self.dispatch(module = new_mission.get('module'), **(new_mission.get('data')))
            self.say('dispatch result is {0}'.format(ret))
            self.say('dispatch finished')
            time.sleep(5)

        self.say('dispatch thread end')


class RegisterThread(threading.Thread):
    """
    register thread, request the URL
    """

    def __init__(self, interval=5, **kwargs):
        super(RegisterThread, self).__init__()
        ##dispatch dict, module and its process thread
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

        self.LOCK = threading.Lock()  # r/w lock for variants

        """
        0: no connection
        1: connected
        2: error in connecting
        """
        self.CONNECTION_STATUS = 0

        ##init other Thread
        try:
            self.__dispath_thread = DispatcherThread()
            self.__dispath_thread.start()

            MyTCPHandler.register_handle_func(self.__dispath_thread.append_to_mission_queue)
            self.__receiver_thread = ReceiverThread()

        except Exception as e:
            self.RUN_FLAG = False
            print('[*] init sub thread error:{0}, quit Register Thread'.format(str(e)))


    def register_module(self, module, callback):
        return self.__dispath_thread.register_module(module, callback)


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
            print('[*] receiver thread init failed, quit Receiver Thread.')
            raise AttributeError('receiver thread init failed, quit Receiver Thread.')

        else:
            print('[*] receiver thread init success with port: %s' % str(self.port))
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
            self.port = random.randint(20000, 60000)
            if self.__start_tcp_server('0.0.0.0', self.port):
                return True
            else:
                retry_count -= 1
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
            if hasattr(self, 'handle_func'):
                print "[*] entering handle_func"

                self.handle_func(in_dict)

            else:
                print "[*] has no handle_func"
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

def summer(x,y):
    print('[*] in sum func: {0}'.format(str(x+y)))


if __name__ == '__main__':
    k = RegisterThread()
    k.register_module(module='print', callback=printer)
    k.register_module(module='sum', callback=summer)
    k.start()
    k.join()
