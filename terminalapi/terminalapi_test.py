import unittest
import time
from terminalapi.terminalapi import DispatcherThread


class LogLevel(object):
    DEBUG = 0
    INFO = 1
    ERROR = 2


class TerminalApiTester(unittest.TestCase):
    def log(self, level=LogLevel.DEBUG, content=''):
        print('[*]' + content)

    def setUp(self):
        pass
        self.log(0, 'start api test')

    def tearDown(self):
        pass
        self.log(0, 'end api test')

    def test_empty_dispatcher(self):
        dispatcher = DispatcherThread()
        dispatcher.start()

        self.assertEqual(len(dispatcher.dispatch_dict), 0, '[!] new dispatcher failed')

        dispatcher.terminate()
        del dispatcher

    def test_register_module_to_dispatcher(self):
        dispatcher = DispatcherThread()
        dispatcher.start()

        test_func = lambda x: x - 1
        module = 'test_func'
        dispatcher.register_module(module=module, callback=test_func)

        print dispatcher.dispatch_dict
        self.assertTrue(dispatcher.dispatch_dict.has_key(module), '[!] dispatcher register failed')

        dispatcher.terminate()
        dispatcher.append_to_mission_queue({'module':'None','data':'None'})
        time.sleep(1)
        del dispatcher

    def test_append_mission_to_queue(self):
        dispatcher = DispatcherThread()
        dispatcher.start()

        minus_func = lambda x: x - 1
        minus_module = 'minus_one'
        dispatcher.register_module(module=minus_module, callback=minus_func)

        sum_func = lambda x,y: x + y
        sum_module = 'sum'
        dispatcher.register_module(module=sum_module, callback=sum_func)

        self.assertTrue(dispatcher.dispatch_dict.has_key(sum_module))
        self.assertTrue(dispatcher.dispatch_dict.has_key(minus_module))

        minus_mission = {'module':'minus_one', 'data':{'x':4}}
        sum_mission = {'module':'sum','data':{'x':5,'y':6}}

        dispatcher.append_to_mission_queue(minus_mission)
        dispatcher.append_to_mission_queue(sum_mission)
        time.sleep(2)
        dispatcher.terminate()
        dispatcher.append_to_mission_queue(sum_mission)
        time.sleep(1)
        del dispatcher

if __name__ == '__main__':
    unittest.main()
