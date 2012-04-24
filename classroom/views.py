# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse


from Server.models import *
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.utils import simplejson
from django.views.decorators.http import require_http_methods

@require_http_methods(['POST'])
def feedback(request):
	feedback = request.POST.get('feedback','-1')
	cid = request.POST.get('keyid',None)
	if cid != None:
		cplace = place.objects.get(keyid=cid)
		cplace.feedback = int(feedback)
		cplace.save()
		return HttpResponse('0')
	return HttpResponse('-1')
		

def jsonBuilding(request):
    	'''there're some bugs here.
    	
	'''		
	result = [{'name':x,'location':i+1} for i,x in enumerate(list_building_old)]
	return HttpResponse(simplejson.dumps(result),mimetype="application/json")
	
@require_http_methods(['POST'])			
def jsonclassroom(request):
	context = {}
	lists = list()
	listt = ()
	building = request.POST.get('building',None)
	day = request.POST.get('day',None)
	c = request.POST.get('c',None)  

	if building != u'99':
		if day != u'99':
			lists = [{'name':cplace.name,'t':cplace.placet_set.filter(weeknumber=c).values(u'day'+day)[0]} \
		    for cplace in place.objects.filter(location=building).order_by('name') if cplace.placet_set.filter(weeknumber=c).count() > 0]
			
	return HttpResponse(simplejson.dumps(list(lists)),mimetype="application/json")
		
		
	
     
