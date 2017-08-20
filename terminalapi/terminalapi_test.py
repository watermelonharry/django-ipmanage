import unittest
from terminalapi.terminalapi import Dispatcher


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
        dispatcher = Dispatcher()
        self.assertEqual(len(dispatcher.dispatch_dict), 0, '[!] new dispatcher failed')

    def test_register_module_to_dispatcher(self):
        dispatcher = Dispatcher()
        test_func = lambda x: x - 1
        module = 'test_func'
        new_one = {module:test_func}
        dispatcher.register_module(module=module, callback=test_func)
        print dispatcher.dispatch_dict
        self.assertTrue(dispatcher.dispatch_dict.has_key(module), '[!] dispatcher register failed')
        self.assertEqual(dispatcher.dispatch(module, 1) , 0, '[!] dispatcher diaspatch mission failed')


if __name__ == '__main__':
    unittest.main()
