from django.conf.urls import url, include
from django.contrib import admin
import views
from rest_framework import routers

app_name='iottest'
urlpatterns = [
    url('^$', views.show_iot_main_page, name='iot_main_page'),
    url('^sutlist/$', views.show_iot_sut_page, name='iot_sut_list_page'),


    url('^api/inner/sutlist/$', views.api_iot_sut_page, name='api_iot_sut_list'),
]
