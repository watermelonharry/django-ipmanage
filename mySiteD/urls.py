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
    url('^about/$', views.show_about_page, name="global_about_page"),
    url('^$', views.hello),
    url('^instools/$',views.show_instance_tool, name='instant_tool'),
    url('^files/',include('filemanage.urls')),
    url('^iottest/',include('iottest.urls')),


    url('^contact/', include('feedback.urls')),

    url('^ipcmanage/', include('ipcmanage.urls')),
    url('^ipcset/', include('ipcset.urls')),
    url('^user/', include('userManage.urls')),
    url('^terminal/', include('terminalReg.urls')),
    url('^iottest/', include('iottest.urls')),

    url(r'^admin/', admin.site.urls),
)
