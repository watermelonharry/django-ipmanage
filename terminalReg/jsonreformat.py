from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


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
