# -*- coding: utf-8 -*-
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