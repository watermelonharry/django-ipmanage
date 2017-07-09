# -*- coding: utf-8 -*-
from django.db import models


class FeedBackModel(models.Model):
	AUTHORITY_CHOICES = (
		(1, u'提交BUG'),
		(2, u'改进建议'),
		(3, u'新需求'),
	)

	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(auto_now=True)

	user_name = models.CharField(max_length=20)
	user_email = models.EmailField(null=True)
	feedback_type = models.IntegerField(choices=AUTHORITY_CHOICES)
	feedback_content = models.TextField()

	def __unicode__(self):
		return self.user_name + self.feedback_content


