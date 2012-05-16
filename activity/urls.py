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

urlpatterns = patterns('Server.activity.views',
    (r'^query$','get_all'),    
    (r'^category$','get_category'),    
    (r'^get$','get_item'),
    (r'^follow$','follow'),
    (r'^following$','get_following')
)

