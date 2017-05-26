# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CnTestEngieer(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    cardNo = models.CharField(max_length=20)
    emailAddr = models.EmailField()
    type = models.IntegerField()

    def __unicode__(self):
        return self.name
    # def __str__(self):
    #     return self.name

class CnCaseInfo(models.Model):
    caseName = models.CharField(max_length=50)
    testSuiteId = models.IntegerField()
    createDate = models.DateTimeField(auto_now_add=True)
    editDate = models.DateTimeField(auto_now=True)
    caseIntroduction = models.TextField()
    editorName = models.ForeignKey(CnTestEngieer)

    def __unicode__(self):
        return self.caseName
    # def __str__(self):
    #     return self.caseName

class CnOperateInfo(models.Model):
    caseName = models.ForeignKey(CnCaseInfo)
    testSuiteName = models.CharField(max_length=50)
    testTime = models.DateField()
    testStatus = models.IntegerField()
    testResult = models.IntegerField()
    testLog = models.TextField()
    operateId = models.IntegerField(unique=True)
    operatorName = models.ForeignKey(CnTestEngieer)

    def __unicode__(self):
        return self.caseName
    # def __str__(self):
    #     return self.caseName


class CnTestSubscribeList(models.Model):
    subscribeTime = models.DateTimeField(auto_now_add=True)
    testName = models.CharField(max_length=50)
    testOwner = models.ForeignKey(CnTestEngieer)
    t_fake_ip = models.CharField(max_length=15)
    t_client_ip = models.CharField(max_length=15,null = True)
    t_qname = models.CharField(max_length=40, null = True)
    testCaseId = models.ManyToManyField(CnCaseInfo)
    level = models.IntegerField(default=0)
    testStatus = models.IntegerField(default=0)
    testLog = models.TextField(null=True)

    def __unicode__(self):
        return self.testName

class CnTestSuiteList(models.Model):
    suiteName = models.CharField(max_length=50)
    developer = models.ForeignKey(CnTestEngieer)
    createTime = models.DateTimeField(auto_now_add=True)
    editTime = models.DateTimeField(auto_now=True)
    suiteIntroduction = models.TextField()

    def __unicode__(self):
        return self.suiteName