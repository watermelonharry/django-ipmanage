from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class BaseResponse(HttpResponse):
    '''
    base HTTP-json response class
    '''

    def __init__(self, data, *args, **kwargs):
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
        super(SuccessJsonResponse, self).__init__(data, *args, **kwargs)

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
        super(ErrorJsonResponse, self).__init__(data, *args, **kwargs)

    def init_content(self, data):
        content_dict = {}
        content_dict['errors'] = data
        content_dict['result'] = u'error'
        return JSONRenderer().render(content_dict)


class FormatJsonParser(JSONParser):
    """
    specific parser for post data
    """

    def __init__(self, stream, *args, **kwargs):
        super(FormatJsonParser, self).__init__()
        self.json_content = super(FormatJsonParser, self).parse(stream)

    def get_ak(self):
        return self.json_content.get('ak', None)

    def get_terminal_name(self):
        return self.json_content.get('terminal_name', None)

    def get_content(self):
        return self.json_content

    def get_data(self):
        return self.json_content.get('data', None)
