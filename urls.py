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


urlpatterns = patterns('Server.views',
	               (r'^$','index'),
	               (r'^classroom/',include('Server.classroom.urls')),
	               (r'^account/',include('Server.account.urls')),
	               (r'^login$','login'),
	               (r'^login_dean$','login_dean'),
	               (r'^login_elective$','login_elective'),

	               (r'^login_portal$','login_portal'),
	               (r'^index$','index'),
	               (r'^course/',include('Server.course.urls')),
	               (r'^app/',include('Server.app.urls')),
	               (r'^manage/',include('Server.manage.urls')),
	               (r'^library/',include('Server.library.urls')),
	               (r'^login_required/','login_required_message')
)
urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
        )
