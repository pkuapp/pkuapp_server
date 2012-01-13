# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
from Server.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import simplejson
from Server.utility.TimeUtil import getTermNumber


@login_required
def json_mycourse(request):
	user=request.user
	courselist=user.course_set.filter(termnumber=getTermNumber()).values('classnum','courseid','id','name','credit','day1','day2','day3','day4','day5','day6','day7','place','rawplace','time','time_test','teachername')
	return HttpResponse(simplejson.dumps(list(courselist)), mimetype='application/json')

@login_required
def json_myprofile(request):
	user=request.user	
	profile=Profile.objects.get(user=user.id)
	context={
	    	'realname':profile.realname,
		'grade':profile.grade,
		'sno':user.username,
		'mphone':profile.mphone,
		'school':profile.school,
		'major':profile.major.strip(' ')
	}
	return HttpResponse(simplejson.dumps(context),mimetype='application/json')

@login_required
def handle_notice(request):
	user=request.user
	if request.method=='POST':
		
		listx=request.POST.get('id','').split(u';')
		try:
			list_id = [int(x)  for x in listx]
		except:
			return HttpResponse('-1')
		for cid in list_id:
			try:					
				cnotice=notice.objects.get(id=cid)
				cnotice.state=True
				cnotice.save()
			except:
				return HttpResponse('-4')
		return HttpResponse('0')
			
	else:
		obj_list=user.notice_set.filter(state=False)
		value_list = list(obj_list.values())
		result_dict = {}
		result_dict['v'] = "0.63"
		for i,obj in enumerate(obj_list):
			context = value_list[i]
			content = obj.getnotice()
			
			context.setdefault('content',content)
			value_list[i] = context
		result_dict['c'] = list(value_list)
		return HttpResponse(simplejson.dumps(result_dict))
	
@login_required
@require_http_methods(['POST'])
def send(request):
	user=request.user
	ccontent=request.POST.get('ct','')
	ctitle=request.POST.get('title','')
	sendto=request.POST.get('to').split(u';')
	cprofile=Profile.objects.get(user=user)
	csms=sms(title=ctitle,content=ccontent,sendfrom=user,sendername=cprofile.realname,state=False)
	csms.save()
	cnotice=notice(sendername=cprofile.realname,state=False,ob=csms.id,ntype=2)
	for x in sendto:
		touser=User.objects.get(id=int(x))
		csms.touser.add(touser)
		cnotice.touser=touser
		csms.save()
		cnotice.save()
	return HttpResponse('0')


@login_required
@require_http_methods(['POST'])
def getsms(request):
	
	user=request.user
	
	smsid=request.POST.get('id','')
	try:
		csms = list(user.inbox.filter(id=smsid).values())[0]
		
		return HttpResponse(simplejson.dumps(csms),mimetype='application/json')
	except:
		return HttpResponse('-4')
	
		
