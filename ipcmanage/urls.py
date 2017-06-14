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
    url('^iptables/$',views.show_ip_table),
    url('^mission_detail/(?P<operate_id>[0-9]+)/$',views.show_mission_datail),
    # url('^caselist/$', views.case_list),
    # url('^testerlist/$', views.tester_list),
    # url('^subscribelist/$', views.subs_list),
    # url('^subscribelist/new$', views.new_test_plan),
    # url('^operateinfo/$', views.operate_list),
    # url('^testsuitelist/(?P<suiteId>\d+)/$', views.testsuite_list),
    # url('^testsuitelist/$', views.testsuite_list),
    # url('^static/assets/css/main.css/$', views.returncss),

    ##api urls
    # url(r'^api/', include(router.urls)),
    # url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/tables/$', views.api_ip_list),
    url(r'^api/tables/(?P<id>[0-9]+)/$', views.api_ip_mac_detail),
    url(r'^api/mission/$', views.api_start_set_ipc),
    url(r'^api/mission/wait/$', views.api_plan_unfinished),
    url(r'^api/mission/(?P<operate_id>[0-9]+)/$', views.api_operate_info),
    url(r'^api/mission/detail/$', views.api_operate_detail),
]
