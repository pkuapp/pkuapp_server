# -*- coding:UTF-8 -*-

from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
from Server.models import *
from Server.settings import MEDIA_ROOT

from elective_handler import run_elective_course_update
from dean_course_handler import run_update_dean_course
from classroom_handler import run_update_classroom   
from django.contrib.auth.decorators import login_required

import urllib
import urllib2
import cookielib
import re    

urlimg="http://elective.pku.edu.cn/elective2008/DrawServlet?Rand=1898.0822409503162"
urllogin="http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/loginServlet/login_webservicehandle.jsp"

def is_staff_required(func):
    def inner(request,*args,**kwargs):
    	if not request.user.is_staff:
    	    return HttpResponse('-14')
    	    
    	else:
    	    	return func(request,*args,**kwargs)
    return inner

def issue(request):
	return HttpResponse('2011/2/21')

def news(request):
	pass

def getTeacherData(request):
	courseset = course.objects.all()
	for ccourse in courseset:
		cname = ccourse.teachername.strip()
		if cname == '':
			continue
		if cname and teacher.objects.filter(name=cname).count() > 0:
			cteacher = teacher.objects.get(name=cname)
			ccourse.teacherid = cteacher
			ccourse.save()
		else:
			cteacher = teacher(name=cname)
			cteacher.save()
			ccourse.teacherid = cteacher
			ccourse.save()
	return HttpResponse('0')

def update_dean_course(request):
	''''''
	error = run_update_dean_course(request)
	return HttpResponse(error)	
	
def update_classroom(request):
	error =	run_update_classroom()
	return HttpResponse(error)	
	
def update_course_elective(request):
	p_notlogin = re.compile(u'未登录')
	if request.method == 'POST':
		data = {}
		data['uid'] = request.POST.get('uid',None)
		data['psd'] = request.POST.get('psd',None)
		data['validCode'] = request.POST.get('validCode',None)
		cookie_value = 'JSESSIONID='+request.POST.get('JSID',None)

		url_values = urllib.urlencode(data)
		request = urllib2.Request(urllogin,url_values)
		request.add_header('Cookie',cookie_value)
		response = urllib2.urlopen(request)
		mlogin = response.read()
		response.close()
		if p_notlogin.search(mlogin):
			return HttpResponse(mlogin)
		error = run_elective_course_update(cookie_value)
		return HttpResponse(error)
		
	else:
		cookieJar=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		JSESSIONID=''
		response=opener.open(urlimg)
		img=response.read()
		
		imgfile=open(MEDIA_ROOT+"elective.gif","w")
		imgfile.write(img)
		imgfile.close()
		for item in cookieJar:
		    if item.name=='JSESSIONID':
			    JSESSIONID=item.value
			    
		context={}
		context['JSID'] = JSESSIONID
		return render_to_response('elective_course.html',context)
			    
def portal(request):
	return render_to_response('portal.html')

@is_staff_required
@login_required
def send_sys_notice(request):
	user = request.user
	title = request.POST.get('title',None)
	content = request.POST.get('content',None)
	sendername = 'PkuCadaMobileDev'
	csys_notice = sys_notice(title=title,content=content,sendername=sendername)
	csys_notice.save()
	user_set = User.objects.all()
	error = ''
	for cuser in user_set:
	    	try:
		    cnotice = notice(obj_id = csys_notice.id,sendername = sendername,ntype=1)
		    cnotice.touser = cuser
		    cnotice.save()
		except:
		    error += 'failed in'+str(cuser.id)
	return HttpResponse('Operation Done'+error)
	
	
