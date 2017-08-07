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
    ## web view urls
    url('^$', views.TerminalListView.as_view(), name='show_terminal_list'),

    ## api urls
    # url('^api/register/$', views.TerminalRegister.as_view(), name='api_terminal_register'),
    url('^api/register/$', views.api_temrinal_register_post, name='api_terminal_register'),
    url('^api/inner/bindterminal/$', views.InnerApiBindMissionTerminal.as_view(), name='api_inner_bind_terminal'),

    url('^api/common/online/$', views.api_outer_get_online_terminal_list, name='api_get_outer_online_terminal_list'),
    url('^api/inner/online/$', views.InnerApiGetOnlineTerminal.as_view(), name='api_get_inner_online_terminal_list'),


    # url('^basic/$',views.show_basic_info),
    #
    # url(r'^api/settings/$', views.api_add_or_get_videosetting),
]
