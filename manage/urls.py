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



urlpatterns = patterns('Server.manage',
			(r'^issue$','views.issue'),
			(r'^news$','views.news'),
	                (r'^getdeancoursedata$','views.update_dean_course'),
	                (r'^getteacherdata$','views.getTeacherData'),
	                (r'^update$','views.update_classroom'),
	                (r'^update_course_elective','views.update_course_elective'),
	                (r'^send_sys_notice$','views.send_sys_notice'),
	                (r'^portal$','view.portal')
			)

