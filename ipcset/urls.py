"""myDTsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'tables', views.api_ip_list)
# router.register(r'^tables/(?P<id>[0-9]+)/$',views.api_ip_mac_detail)

urlpatterns = [
    url('^$', views.welcome),
    url('^basic/$',views.show_basic_info),
    url('^basic/model/$',views.show_basic_model_info),
    url('^settings/$', views.show_settings_info),
    url('^settings/download/$', views.download_settting_table, name='download_video_setting'),
    url('^missions/$', views.show_mission_info),
    url('^missions/(?P<mid>[0-9]+)/$', views.show_mission_detail_info),

    url(r'^api/settings/$', views.api_add_or_get_videosetting),
    url(r'^api/settings/sync/$', views.api_sync_stream_setting),
    url(r'^api/settings/sametype/$', views.api_get_same_type_by_id),
    url(r'^api/settings/batch/$', views.api_batch_detele_videosetting),
    url(r'^api/settings/(?P<id>[0-9]+)/$', views.api_edit_single_videosetting),
    url(r'^api/basic/model/$', views.api_get_model_type),
    url(r'^api/mission/$', views.api_get_add_put_mission),
    url(r'^api/mission/assign/$', views.api_get_waiting_mission),
    url(r'^api/mission/info/(?P<mid>[0-9]+)/$', views.api_get_mission_by_mid),
    url(r'^api/mission/(?P<mid>[0-9]+)/$', views.api_get_add_put_mission_detail),
    url(r'^api/mission/discover/(?P<mid>[0-9]+)/$', views.api_add_put_discover_mission_detail),

    url(r'^api/model/query/', views.api_query_params_by_model),
]
