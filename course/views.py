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
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from Server.utility import TimeUtil
import datetime

categorylist = [u'全校任选',u'全校必修',u'通选课',u'院系课程']
SchoolList = School.objects.all().values('name','code')
dthandler = lambda obj:obj.isoformat() if isinstance(obj,datetime.datetime) else None


@login_required
@require_http_methods(['POST',])
def course_detail(request):
	cid = request.POST.get('id',None)
	try:
		course_values = list(course.objects.filter(id=cid).values())[0]
	except:
		return HttpResponse('-4')
	return HttpResponse(simplejson.dumps(course_values),mimetype='application/json')
	
@login_required
@require_http_methods(['POST',])
def comment_course(request):
	message = '0'
	user = request.user
	content=request.POST.get('content',None)
	cid=request.POST.get('id',None)
	if content == '':
		return HttpResponse(message)
	ccomment=comment(content=content,sendername=Profile.objects.get(user=user).realname)
	ccomment.user=user
	ccomment.save()
	try:
		ccourse=course.objects.get(id=int(cid))
		ccomment.course=ccourse
		ccomment.save()
	except:
		message ='-4'
	try:
		ccourse=course.objects.get(id=int(cid))
		cplace=ccourse.place
		ccomment.place=cplace
		ccomment.save()
	except:
		message ='-4'
		
	return HttpResponse(message)
	
@login_required
@require_http_methods(['POST'])
def comment_detail(request):
	cid = request.POST.get('id','')
	try:
		comment_values = comment.objects.filter(id=int(cid)).values()
		dict_comment = list(comment_values)[0]
	except:
		return HttpResponse('-4')
	return HttpResponse(simplejson.dumps(dict_comment,default=dthandler),mimetype='application/json')




@require_http_methods(['POST'])
def comment_query(request):
	message = '0'
	list_values = list()
	list_objects = list()
	cid = request.POST.get('id',None)
	beg = request.POST.get('beg','0')
	end = request.POST.get('end','5')
	try:
		list_objects_all = comment.objects.filter(course=int(cid))
		list_objects = list_objects_all[int(beg):int(end)]
		list_values = list_objects.values()
		num = list_objects_all.count()
	
		list_results= list()
			
		for i,objectx in enumerate(list_objects):
			list_results.append({'c':list_values[i],'num':objectx.reply_set.all().count()})
	except:
		return HttpResponse('-4')	
		
	return HttpResponse(simplejson.dumps({'list':list(list_results),'num':num},default=dthandler),mimetype='application/json')
	
@login_required
@require_http_methods(['POST'])
def reply_comment(request):
	user = request.user
	cid = request.POST.get('id','')
	uid = request.POST.get('uid','')
	content = request.POST.get('content','')
	if content == '':
		return HttpResponse(message)

	try:
		tocomment = comment.objects.get(id=int(cid))
	except:
		return HttpResponse('-41')
	try:
		touser = User.objects.get(id=int(uid))
	except:
		return HttpResponse('-42')
	try:
		sendername = Profile.objects.get(user=user).realname
		
	except:
		return HttpResponse('-43')	
		
	try:	
		touser_name = Profile.objects.get(user=touser).realname
	except:
		return HttpResponse('-45')	
	
	creply = reply(tocomment=tocomment,touser=touser,sendername=sendername,sendfrom=user,content=u"回复"+touser_name+":"+content)
	creply.save()
	if user != touser:
		cnotice = notice(sendername=sendername,state=False,obj_id=tocomment.id,ntype=0)
		cnotice.touser = touser
		cnotice.save()
	
	commentUser = tocomment.user
	if commentUser != touser and user != commentUser:
		cnotice = notice(sendername=sendername,state=False,obj_id=tocomment.id,ntype=0)
		cnotice.touser = commentUser
		cnotice.save()
	try:
		pass		
	except:
		return HttpResponse('-4')
	
	
	return HttpResponse('0')

@login_required
@require_http_methods(['POST'])
def reply_query(request):
	cid = request.POST.get('id','')
	beg = request.POST.get('beg','0')
	end = request.POST.get('end','5')
	try:
		ccomment = comment.objects.get(id=int(cid))
		list_reply = ccomment.reply_set.values()[int(beg):int(end)]
	except:
		return HttpResponse('-4')
	return HttpResponse(simplejson.dumps(list(list_reply),default=dthandler),mimetype='application/json')


@require_http_methods(['POST'])
def query_course_detail(request):
	cid = request.POST.get('id',None)
	if cid :
		dataCourse = course.objects.get(id = int(cid)).values()
		return HttpResponse(simplejson.dumps(dataCourse),mimetype='application/json')
	return HttpResponse('-3')		
	
def query_category(request):
	term = TimeUtil.getTermNumber()
	SchoolList = list(School.objects.all().values('name','code'))
	categoryData = [u'全校任选',u'全校必修',u'通选课',u'双学位',u'辅修',SchoolList]
	return HttpResponse(simplejson.dumps(categoryData),mimetype='application/json')

@require_http_methods(['POST'])
def query_course_fromCategory(request):
	term = TimeUtil.getTermNumber()
	category = request.POST.get('type',u'全校任选')
	code = request.POST.get('code',None)
	if code:
		courseData = ls(course.objects.filter(SchoolCode = code,termnumber = term))
	else:
		courseData = ls(course.objects.filter(Coursetype = category,termnumber = term))
	
	return HttpResponse(simplejson.dumps(courseData),mimetype='application/json')

def ls(queryset):
		return list(_removeExtraKey(queryset.values('Coursetype','SchoolCode','txType','id','classnum','courseid','time_test','time','name','credit','teachername','rawplace',*['day'+str(x+1) for x in range(7)])))

def query_course_all2(request):
	
	term = TimeUtil.getTermNumber()
	queryset = course.objects.filter(termnumber = term)
	
	SchoolList = School.objects.all().values_list('name','code')
	SchoolContext = {}
	for (name,code) in SchoolList:
		SchoolContext[name] = ls(queryset.filter(SchoolCode = code))
	
	courseData = {u'全校任选':ls(queryset.filter(Coursetype='全校任选')),u'全校必修':ls(queryset.filter(Coursetype='全校必修'))\
	,u'通选课':ls(queryset.filter(Coursetype='通选课')),u'双学位':ls(queryset.filter(Coursetype='双学位')),u'辅修':ls(queryset.filter(Coursetype='辅修')),u'院系课程':SchoolContext}
	
	return HttpResponse(simplejson.dumps(courseData),mimetype='application/json')
	
def query_course_all(request):
	term = TimeUtil.getTermNumber()
	queryset = course.objects.filter(termnumber = term).order_by('name')
	return HttpResponse(simplejson.dumps(ls(queryset)),mimetype='application/json')	
			
def _removeExtraKey(queryset):
	
	for coursedict in queryset:
		
		for dayx in ['day'+str(x+1) for x in range(7)]:
			if 0 == coursedict[dayx]:
				del coursedict[dayx]
				
	return queryset	
		
def getteacherall(request):
	values = list(teacher.objects.all().values())
	return HttpResponse(simplejson.dumps(values),mimetype='application/json')
	
     
