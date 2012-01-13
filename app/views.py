from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
from Server.models import sys_notice
from django.utils import simplejson
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

def getpkutime(request):
	return HttpResponse('2011/9/5')

def get_pku_end_time(request):
    return HttpResponse('2011/12/26')

def get_sys_notice(request):
	cid = request.POST.get('id',None)
	cnotice = sys_notice.objects.get(id=cid)
	return HttpResponse(simplejson.dumps(model_to_dict(cnotice)),mimetype='application/json')

def getAndroidVersion(request):
	pass
