from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mySiteD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^hello/$', hello),
    url('^$', hello),

    url('^time/$', time),
    url('^pretest/$', pre_test),
    url('^dnstest/', include('dnstest.urls')),

    url('^usermanage/', include('userManage.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^register/', register),
)
