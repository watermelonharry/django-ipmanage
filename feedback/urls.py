from django.conf.urls import url, include
from django.contrib import admin
import views
from rest_framework import routers

app_name='feedback'
urlpatterns = [
    url('^$', views.write_contact, name='feedback_submit'),
]
