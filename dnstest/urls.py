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
from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url('^caselist/$', views.case_list),
    url('^testerlist/$', views.tester_list),
    url('^subscribelist/$', views.subs_list),
    url('^subscribelist/new$', views.new_test_plan),
    url('^operateinfo/$', views.operate_list),
    url('^testsuitelist/(?P<suiteId>\d+)/$', views.testsuite_list),
    url('^testsuitelist/$', views.testsuite_list),
]
