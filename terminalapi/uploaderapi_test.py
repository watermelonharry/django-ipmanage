# -*- coding: UTF-8 -*
"""
__VERSION__ = '2017.10.12'
__author__ = 'heyu'

description: unittest for module uploaderapi
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
    import unittest
    from uploaderapi import UploaderThread, UploadDataFormatter
except Exception as e:
    print('[*] import error:' + e.message)
    raise e

"""
Globals here
"""

"""
log settings
"""
formatter = logging.Formatter("%(asctime)s- %(levelname)s- %(name)s- %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("terminal.log")
file_handler.setFormatter(formatter)

"""
classes here
"""


class LogLevel(object):
    DEBUG = 0
    INFO = 1
    ERROR = 2


class UploaderThreadTester(unittest.TestCase):
    def log(self, content='', level=LogLevel.DEBUG):
        if level == LogLevel.DEBUG:
            prifix = "debug:"
        elif level == LogLevel.INFO:
            prifix = 'info:'
        elif level == LogLevel.ERROR:
            prifix = 'error:'
        print(u'[*] {0}{1}'.format(prifix, content))

    def setUp(self):
        self.log('start api test')

    def tearDown(self):
        self.log('end api test')
    #
    # def test_init_uploader(self):
    #     uploader = UploaderThread(ak="123214123")
    #     self.assertTrue(isinstance(uploader, UploaderThread))
    #     self.assertEqual(uploader.ak, '123214123')

    # def test_post_test(self):
    #     uploader = UploaderThread(ak="123214123")
    #     post_data = {'dst_url':"http://127.0.0.1:8000/iottest/api/test/", 'data':{"v1":"nanana","v2":"bobbo"}, 'expected_reply':200, 'method':"POST"}
    #     get_data = {'dst_url':"http://127.0.0.1:8000/iottest/api/test/", 'data':{"v1":"nanana","v2":"bobbo"}, 'expected_reply':200, 'method':"GET"}
    #     put_data = {'dst_url':"http://127.0.0.1:8000/iottest/api/test/", 'data':{"v1":"nanana","v2":"bobbo"}, 'expected_reply':200, 'method':"PUT"}
    #     delete_data = {'dst_url':"http://127.0.0.1:8000/iottest/api/test/", 'data':{"v1":"nanana","v2":"bobbo"}, 'expected_reply':200, 'method':"DELETE"}
    #     uploader.start()
    #     uploader.push_to_queue(data=post_data)
    #     uploader.push_to_queue(data=get_data)
    #     uploader.push_to_queue(data=put_data)
    #     uploader.push_to_queue(data=delete_data)
    #     # time.sleep(10)
    #     # uploader.terminate_thread()

    def test_formatter_get_post_data(self):
        f = UploadDataFormatter(ak="12341123", terminal_name='test_terminal')
        content= f.get_format_post_data(data={"v1":1234,"v2":5678})
        self.assertEqual(content['data'], {"v1":1234,"v2":5678})
        self.assertEqual(content['ak'], '12341123')
        self.assertEqual(content['terminal_name'], 'test_terminal')
        self.assertEqual(content['offset'], 0)
        self.assertEqual(content['limit'], 10)

    def test_formatter_get_Get_data(self):
        f = UploadDataFormatter(ak="12341123", terminal_name='test_terminal')
        content= f.get_format_get_data(data={"v1":1234,"v2":5678})
        self.assertEqual(content['data'], {"v1":1234,"v2":5678})
        self.assertEqual(content['ak'], '12341123')
        self.assertEqual(content['terminal_name'], 'test_terminal')
        self.assertEqual(content['offset'], None)
        self.assertEqual(content['limit'], None)