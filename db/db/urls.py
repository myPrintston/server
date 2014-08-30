from django.conf.urls import patterns, include, url
from django.contrib import admin
from authviews import *
from views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'db.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^pall/$', allPrinters),
    url(r'^etypes/$', allErrorTypes),
    url(r'^pid/(\d+)/$', onePrinterStatus),
    url(r'^pallStat/$', allPrinterStatuses),
    url(r'^error/$', addError),
    url(r'^pids/(?P<args>[0-9/]+)/$', printerStatuses),
    url(r'^login/(?P<username>.*)/(?P<password>.*)/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^checklogin/$', checklogin),
    url(r'^fixprinter/(\d+)/$', fixPrinter),
    url(r'^geterrors/(?P<pid>[0-9]+)/$', getErrors),
    url(r'^fixerrors/(?P<pid>[0-9]+)/(?P<eid>[0-9/]+)/$', fixErrors),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
