# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.



class UserModel(models.Model):
    AUTHORITY_CHOICES = (
        (1, u'管理员'),
        (2, u'测试人员'),
        (3, u'观察员'),
    )

    creatTime = models.DateTimeField(auto_now_add= True)
    editTime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    cardNo = models.CharField(max_length=20)
    emailAddr = models.EmailField(null = True)
    auth = models.IntegerField(choices=AUTHORITY_CHOICES)
    otherInfo = models.TextField()

    def __unicode__(self):
        return self.name