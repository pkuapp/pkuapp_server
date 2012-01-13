#/*from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#urlpatterns = patterns('',
    # Example:
    # (r'^test1/', include('test1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
#)
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import * 
from django.contrib import admin



urlpatterns = patterns('',
			(r'^date$','Server.app.views.getpkutime'),
			(r'^enddate$','Server.app.views.get_pku_end_time'),
			(r'^sys_notice$','Server.app.views.get_sys_notice'),
			)

