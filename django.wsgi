import os, sys

sys.path.append('/Library/WebServer/Documents')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Server.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()