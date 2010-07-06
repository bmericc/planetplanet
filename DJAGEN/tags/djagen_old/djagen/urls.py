from django.conf.urls.defaults import *
from djagen.collector.views import *
from djagen import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^archive/$',archive),
    (r'^archive/(?P<archive_year>\d{4})/$', archive),
    (r'^archive/(?P<archive_year>\d{4})/(?P<archive_month>\d{1,2})/$', archive),
    (r'^djagen/$',main),
    
    # For development server.
    #(r'^(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.BASEPATH + 'gezegen/www/'}),
    

)