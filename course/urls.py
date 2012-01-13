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

urlpatterns = patterns('Server.course.views',
	               (r'^comment$','comment_course'),    
	               (r'^reply$','reply_comment'),    
	               (r'^query_comment$','comment_query'),
	               (r'^query_reply$','reply_query'),
	               (r'^all$','query_course_all'),
	               (r'^category$','query_category'),
	               (r'^query$','query_course_fromCategory'),
	               (r'^comment/detail$','comment_detail'),
	               (r'^detail$','course_detail')
)

