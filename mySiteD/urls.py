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

    url('^dnstest/', include('dnstest.urls')),

    url('^ipcmanage/', include('ipcmanage.urls')),
    url('^ipcset/', include('ipcset.urls')),
    url('^user/', include('userManage.urls')),

    # url('^usermanage/', include('userManage.urls')),

    url(r'^admin/', admin.site.urls),
)
