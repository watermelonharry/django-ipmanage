from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class BaseResponse(HttpResponse):
	'''
	用来返回json数据
	'''

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(BaseResponse, self).__init__(content, **kwargs)
