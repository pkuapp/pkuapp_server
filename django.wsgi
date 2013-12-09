import os, sys
sys.path.append(r'/var')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Server.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
