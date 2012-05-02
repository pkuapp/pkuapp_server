from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
from Server.models import sys_notice
from django.utils import simplejson
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

def getpkutime(request):
	return HttpResponse('2012/2/13')

def get_pku_end_time(request):

    return HttpResponse('2012/6/10')

def getServerStatus(request):
	return HttpResponse(simplejson.dumps({'status':0,'date_start':'2012/2/13','date_end':'2012/6/10'}),mimetype='application/json')

def get_sys_notice(request):
	cid = request.POST.get('id',None)
	cnotice = sys_notice.objects.get(id=cid)
	return HttpResponse(simplejson.dumps(model_to_dict(cnotice)),mimetype='application/json')

def Android_version(request):
	return HttpResponse(simplejson.dumps({'v':"0.632"}),mimetype='application/json')

def iOS_version(request):
    return HttpResponse(simplejson.dumps({'beta':90}),mimetype='application/json')

def WP_version(request):
    return HttpResponse(simplejson.dumps({'v':"0.1"}),mimetype='application/json')
