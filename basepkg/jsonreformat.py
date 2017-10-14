from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json


class BaseResponse(HttpResponse):
    '''
    base HTTP-json response class
    '''

    def __init__(self, data, *args, **kwargs):
        if data is None:
            content = self.init_content({"error": "please input dict"})
        else:
            content = self.init_content(data)

        kwargs['content_type'] = 'application/json'
        super(BaseResponse, self).__init__(content, **kwargs)

    def init_content(self, data):
        return JSONRenderer().render(data)


class SuccessJsonResponse(BaseResponse):
    """
    success HTTP-json response.
    jsonfy the key-value dict into json string and wrapped as HTTP response.
    """

    def __init__(self, data, *args, **kwargs):
        if 'status' in kwargs:
            super(SuccessJsonResponse, self).__init__(data, *args, **kwargs)
        else:
            super(SuccessJsonResponse, self).__init__(data, status=200, *args, **kwargs)

    def init_content(self, data):
        content_dict = {}
        content_dict['data'] = data
        content_dict['result'] = u'success'
        return JSONRenderer().render(content_dict)


class ErrorJsonResponse(BaseResponse):
    """
    error HTTP-json response.
    jsonfy the key-value dict into json string and wrapped as HTTP response.
    """

    def __init__(self, data, *args, **kwargs):
        # todo: status_code modify
        if 'status' in kwargs:
            super(ErrorJsonResponse, self).__init__(data, *args, **kwargs)
        else:
            super(ErrorJsonResponse, self).__init__(data, status=400, *args, **kwargs)

    def init_content(self, data):
        content_dict = {}
        content_dict['errors'] = data
        content_dict['result'] = u'error'
        return JSONRenderer().render(content_dict)


class FormatJsonParser(object):
    """
    specific parser for post data
    """

    def __init__(self, stream, *args, **kwargs):
        self.content = {}
        for method in ("GET", "POST", "PUT", "DELETE"):
            try:
                setattr(self, u'{0}_content'.format(method), eval('stream.{0}'.format(method)))
            except Exception as e:
                setattr(self, u'{0}_content'.format(method), {})
            self.content.update(eval("self.{0}_content".format(method)))

        try:
            self.body_content = JSONParser().parse(stream)
            if isinstance(self.body_content, (str, unicode)):
                self.body_content = json.loads(self.body_content)
        except Exception as e:
            self.body_content = {}

        self.content.update(self.body_content)

    def get_ak(self):
        return self.content.get('ak', None)

    def get_terminal_name(self):
        return self.content.get('terminal_name', None)

    def get_content(self):
        temp_dict = {}
        temp_dict.update(self.content)
        return temp_dict

    def get_data(self):
        return self.get('data', None)

    def __getattr__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            val = self.content.get(item, None)
            return val
