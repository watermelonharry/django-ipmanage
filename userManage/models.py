# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class UserModel(models.Model):
	AUTHORITY_CHOICES = (
		(1, u'管理员'),
		(2, u'测试人员'),
		(3, u'观察员'),
	)

	creatTime = models.DateTimeField(auto_now_add=True)
	editTime = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=20)
	gender = models.CharField(max_length=10, )
	cardNo = models.CharField(max_length=20)
	emailAddr = models.EmailField(null=True)
	auth = models.IntegerField(choices=AUTHORITY_CHOICES)
	otherInfo = models.TextField()

	def __unicode__(self):
		return self.name


class ApiKeyModel(models.Model):
	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	api_key = models.CharField(max_length=50, unique=True)  ##hash key
	user_id = models.IntegerField()  ##user id in auth.user table

	def __unicode__(self):
		return unicode(self.user_id) + u'-' + unicode(self.api_key[:10])

	def validate(self, input_key):
		"""
		verify if the input api_key equals the users key
		:param input_key:
		:return:
		"""
		if input_key == self.api_key:
			return True
		else:
			return False
