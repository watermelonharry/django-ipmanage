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
    url('^$', views.web_welcome, name="ipmanage_main_page"),
    url('^config/$', views.web_config_page, name="ipmanage_config_page"),
    url('^config/(?P<id>[0-9]+)/$', views.web_config_detail_page, name="ipmanage_config_detail_page"),

    # inner api
    url('^api/v1/config/$', views.api_get_config_list, name="ipmanage_api_config_list"),
    url('^api/v1/config/detail/$', views.api_get_config_detail_list, name="ipmanage_api_config_detail_list"),

    # terminal api

    # url('^iptables/$',views.show_ip_table),
    # url('^iptables/download/$',views.download_iptables),
    # url('^mission_detail/(?P<operate_id>[0-9]+)/$',views.show_mission_datail),
    # url('^mission/$',views.show_mission_info),
    #
    # ##api urls
    # url(r'^api/tables/$', views.api_get_add_put_ip_mac_table),
    # url(r'^api/tables/(?P<id>[0-9]+)/$', views.api_get_put_single_mac),
    # url(r'^api/mission/$', views.api_post_mission_info),
    # url(r'^api/mission/wait/$', views.api_plan_unfinished),
    # url(r'^api/mission/(?P<operate_id>[0-9]+)/$', views.api_put_get_delete_mission_info),
    # url(r'^api/mission/detail/$', views.api_post_mission_detail),
]
