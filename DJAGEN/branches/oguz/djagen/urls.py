from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djagen/', include('djagen.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^main/', 'djagen.collector.views.main'),
    (r'^subscribe/', 'djagen.collector.views.member_subscribe'),
    (r'^members/', 'djagen.collector.views.list_members'),
)
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)
