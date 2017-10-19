# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser



# Create your models here.





class ApiKeyModel(models.Model):
	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	key_chain = models.CharField(max_length=50, unique=True)  ##hash key
	user_id = models.IntegerField()  ##user id in auth.user table

	def __unicode__(self):
		return unicode(self.user_id) + u'-' + unicode(self.key_chain[:10])

	def validate(self, input_key_chain):
		"""
		verify if the input api_key equals the users key
		:param input_key:
		:return:
		"""
		if input_key_chain == self.key_chain:
			return True
		else:
			return False

	@classmethod
	def get_model_by_ak(cls, input_key_chain):
		try:
			return cls.objects.get(key_chain=input_key_chain)
		except:
			return None

	@classmethod
	def has_ak(cls, ak=None, data=None):
		"""
		verify the request data carries valid ak
		:param request:
		:return:
		"""
		try:
			if data:
				terminal_ak = data.get('ak', '')
			if ak:
				terminal_ak = ak
			api_model = cls.get_model_by_ak(terminal_ak)
			if not api_model:
				return None
			else:
				return api_model
		except Exception as e:
			return None


class UserApiModel(User):
	other_info = models.TextField(blank=True)
	api_key_model = models.ForeignKey(ApiKeyModel, blank=True, null=True)

	def __unicode__(self):
		return self.username

	def validate_api_key(self, input_api_key, **kwargs):
		"""
		validate api key by input key string
		:param input_api_key:
		:param kwargs:
		:return:
		"""
		try:
			if self.api_key.key_chain == input_api_key:
				return True
			else:
				return False
		except Exception as e:
			return False

	def generate_api_key(self):
		"""
		genetare api key based on username.password.random
		:return:
		"""
		try:
			import random
			import hashlib
			gene_hash = lambda x: hashlib.sha1(unicode(x)).hexdigest()

			salt = gene_hash(random.random())[:20]
			sha_key = gene_hash(self.username[:10] + salt + self.password[:10])[:20]

			new_api_key_model = ApiKeyModel(user_id=self.id,
			                                key_chain=sha_key)
			new_api_key_model.save()

			self.api_key_model = new_api_key_model
			return sha_key
		except Exception as e:
			return None

	def update_api_key(self):
		"""
		generate new api_key for the user
		:return:
		"""
		try:
			self.api_key_model.delete()
			if self.generate_api_key():
				self.save()
				return True
			else:
				return None
		except Exception as e:
			return None


def validate_api_key(username, api_key):
	"""
	validate api key by input username and api_key
	:param username:
	:param api_key:
	:return: True or False
	"""
	try:
		user = UserApiModel.objects.get(username=username)
		if user.api_key_model.key_chain == api_key:
			return True
		else:
			return False
	except Exception as e:
		return False
