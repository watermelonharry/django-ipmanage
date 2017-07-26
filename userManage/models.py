# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


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


class UserApiModel(User):
	other_info = models.TextField(blank=True)
	api_key_model = models.ForeignKey(ApiKeyModel, blank=True, null=True)

	def __unicode__(self):
		return self.username

	def validate_api_key(self, input_api_key):
		try:
			if self.api_key.key_chain == input_api_key:
				return True
		except Exception as e:
			pass
		finally:
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
			sha_key = gene_hash(self.username[:10] + salt + self.password[:10])[:15]

			new_api_key_model = ApiKeyModel(user_id=self.id,
			                                key_chain=sha_key)
			new_api_key_model.save()

			self.api_key_model = new_api_key_model
			return sha_key
		except Exception as e:
			return None
