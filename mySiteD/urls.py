from django.conf.urls import patterns, include, url

from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mySiteD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^hello/$', views.hello),
    url('^$', views.hello),


    url('^contact/', include('feedback.urls')),
    # url('^dnstest/', include('dnstest.urls')),

    url('^ipcmanage/', include('ipcmanage.urls')),
    url('^ipcset/', include('ipcset.urls')),
    url('^user/', include('userManage.urls')),
    url('^terminal/', include('terminalReg.urls')),
    url('^iottest/', include('iottest.urls')),

    url(r'^admin/', admin.site.urls),
)
