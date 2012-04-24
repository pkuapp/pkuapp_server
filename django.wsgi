import os, sys
sys.path.append(r'D:\CADA\website\admin\mobile')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Server.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()