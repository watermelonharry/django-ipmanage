from django.conf.urls import url, include
from django.contrib import admin
import views
from rest_framework import routers

app_name = 'iottest'
urlpatterns = [
    url('^$', views.show_iot_main_page, name='iot_main_page'),
    url('^sutlist/$', views.show_iot_sut_page, name='iot_sut_list_page'),
    url('^missionlist/$', views.show_mission_list, name='iot_mission_list_page'),
    url('^missiondetail/(?P<m_id>[0-9]+)/$', views.show_mission_detail, name='iot_mission_detail_page'),
    url('^missioncompare/$', views.show_mission_compare, name='iot_mission_compare_page'),

    url('^api/v1/inner/suts/$', views.api_get_add_iot_suts, name='api_get_add_iot_suts'),
    url('^api/v1/outter/suts/$', views.api_out_get_add_iot_suts, name='api_out_get_add_iot_suts'),
    url('^api/v1/inner/suts/ids/$', views.api_get_iot_sut_ids, name='api_get_iot_suts_ids'),

    url('^api/v1/inner/missions/$', views.api_get_add_put_delete_missions, name='api_get_add_put_delete_missions'),
    url('^api/v1/outter/missions/$', views.api_outter_get_add_put_delete_missions,
        name='api_outter_get_add_put_delete_missions'),

    url('^api/v1/outter/missionprogress/(?P<m_id>[0-9]+)/$', views.api_out_get_mission_progress),
    url('^api/v1/inner/missionprogress/(?P<m_id>[0-9]+)/$', views.api_get_mission_progress,
        name='api_get_mission_progress'),

    url('^api/v1/inner/missiondetails/(?P<m_id>[0-9]+)/$', views.api_get_add_mission_details,
        name='api_get_add_mission_details'),
    url('^api/v1/outter/missiondetails/(?P<m_id>[0-9]+)/$', views.api_outter_get_add_mission_details),

    url('^api/v1/inner/missioncompare/$', views.api_inner_compare_two_mission),


    url('^api/v1/test/$', views.api_test_receive_url, name='test_api_url'),
]
