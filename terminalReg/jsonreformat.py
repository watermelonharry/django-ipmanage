from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class BaseResponse(HttpResponse):
	'''
	base HTTP-json response class
	'''

	def __init__(self, data, *args, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(BaseResponse, self).__init__(content, **kwargs)


class SuccessJsonResponse(BaseResponse):
	"""
	success HTTP-json response.
	jsonfy the key-value dict into json string and wrapped as HTTP response.
	"""

	def __init__(self, data, *args, **kwargs):
		pass


class ErrorJsonResponse(BaseResponse):
	"""
	error HTTP-json response.
	jsonfy the key-value dict into json string and wrapped as HTTP response.
	"""
	def __init__(self, data, *args, **kwargs):
		pass
