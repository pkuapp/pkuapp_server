# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
import urllib
import urllib2
import cookielib
from Server.models import Profile
import BeautifulSoup
from env.env import *
from env.urlmap import *
from django.contrib import auth
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import re
from account_handler import handle_course,dict_deanprofile
from django.views.decorators.http import require_http_methods
from utility.TimeUtil import getTermNumber
from Server.settings import MEDIA_ROOT
import MasterStu_handler
import Stu_elective_handler

"这是教务登陆后返回的字串里包含的一条信息，用于识别是否成功登陆"
plogin=re.compile(u'parent\.location\.href="student_index\.php\?PHPSESSID')


def _loginFromData(request,data):

	user = authenticate(username = data['sno'],password = data['passwd'])
	if user is not None:
		if user.is_active:
			auth_login(request,user)
			return HttpResponse('0')
		else:
			return HttpResponse('-1')
	return HttpResponse('-202')

def login_dean_with_data(**kwarg):
	data = kwarg['data']
	PHPSESSID = kwarg['PHPSESSID']
	request = kwarg['request']
    	headers={'User-Agent':user_agent,'PHPSESSID':PHPSESSID}
    	if data['number']==u'':
		return _loginFromData(request,data)
	else:		
		url_values=urllib.urlencode(data)
		req=urllib2.Request(urlin+PHPSESSID,url_values,headers)
		response=urllib2.urlopen(req)
		logindata=response.read()
		response.close()
		if re.search(plogin,logindata.decode('gb18030')):
			'''get course data'''
			req=urllib2.Request(urlxkqk+PHPSESSID,None,headers)
			response=urllib2.urlopen(req)
			doc_xkqk=response.read().decode('GBK')
			'''get profile from dean'''
			req=urllib2.Request(urlprofile+PHPSESSID,None,headers)
			response=urllib2.urlopen(req)
			doc_profile=response.read().decode('GBK')
			'''退出'''
			req=urllib2.Request(urlexit+PHPSESSID)
			urllib2.urlopen(req)
			response.close()
			register={}
			register = dict_deanprofile(doc_profile)
			'''if user does not exists yet'''
			if User.objects.filter(username=data['sno']).count() == 0:
				
				userprofile = Profile(realname=register.get('realname',''),
					school = register.get('school',''),
					grade = register.get('grade',''),
					major = register.get('major',''),
					mphone = register.get('mphone',''),
					phone = register.get('phone',''),
					user_type = 0
					)
				user = User.objects.create_user(username=data['sno'],password=data['passwd'],email=register.get('email','example@example.com'))
				user.save()

				userprofile.user=user
				userprofile.save()

				'''begin handle course data'''
				try:
					pass
					error = handle_course(doc_xkqk,user)
				except:
					return HttpResponse('-5')
				
				
				return _loginFromData(request,data)
			else:
				cuser = User.objects.get(username=data['sno'])
				cuser.set_password(data['passwd'])
				try:
					profile = Profile.objects.get(user=cuser.id)
				except:
					profile = Profile(realname=register.get('realname',''),
						school = register.get('school',''),
						grade = register.get('grade',''),
						major = register.get('major',''),
						mphone = register.get('mphone',''),
						phone = register.get('phone',''),
						user_type = 0
					)
				profile.realname = register.get('realname','')
				profile.school = register.get('school','')
				profile.grade = register.get('grade','')
				profile.grade = mphone = register.get('mphone','')
				profile.phone = register.get('phone','')
				profile.user_type = 0;
				profile.save()
				course_set = cuser.course_set.filter(termnumber = getTermNumber())
				
				for ccourse in course_set:
					ccourse.user.remove(cuser)
					ccourse.save()
				cuser.save()
				error = handle_course(doc_xkqk,cuser)
				return _loginFromData(request,data)
		else:
		    '''exit'''
		    req=urllib2.Request(urlexit+PHPSESSID)
		    urllib2.urlopen(req)
		    response.close()
		    error = logindata.decode('gb18030')
		    return HttpResponse('<!--'+error+'-->')
	return HttpResponse('-1')

@require_http_methods(['POST'])
def login_dean(request):
		
	data={}
	PHPSESSID=request.POST.get('sessionid','')
	data['database']='0'
	data['sno']=request.POST.get('username','')
	data['passwd']=request.POST.get('passwd','')
	data['number']=request.POST.get('valid','')
	return login_dean_with_data(**locals())

	

def login(request):
   	data={}
	PHPSESSID=request.POST.get('sid','')
	data['database']='0'
	data['sno']=request.POST.get('sno','')
	data['passwd']=request.POST.get('pwd','')
	data['number']=request.POST.get('check','')
	return login_dean_with_data(**locals())



@require_http_methods(['POST'])
def login_elective(request):
	def _login(request):
		user = authenticate(username = request.POST.get('username',''),\
			password = request.POST.get('passwd',''))
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return HttpResponse('0')
			else:
				return HttpResponse('-1')
		return HttpResponse('-202')
	
	urlCourseResults = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/electiveWork/showResults.do'
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	urllogin_elective="http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/loginServlet/login_webservicehandle.jsp"
	p_login = re.compile(u'([^ ]*) *([^ ]*) 您好')
	p_notlogin = re.compile(u'未登录')
	if request.method == 'POST':
		data = {}
		data['uid'] = request.POST.get('username',None)
		data['psd'] = request.POST.get('passwd',None)
		data['validCode'] = request.POST.get('valid',None)
		cookie_value = 'JSESSIONID='+request.POST.get('sessionid',None)

		url_values = urllib.urlencode(data)
		_req = urllib2.Request(urllogin_elective,url_values)
		_req.add_header('Cookie',cookie_value)
		response = urllib2.urlopen(_req)
		mlogin = response.read().decode('utf8')
		response.close()
		match_login = p_login.search(mlogin)
		# return HttpResponse(mlogin)
		if match_login:
			register = {}
			register['realname'] = match_login.group(2)
			register['school'] = match_login.group(1)
			'''Get Course Doc'''
			
			'''退出'''
			# no need
			
			'''if user does not exists yet'''
			if User.objects.filter(username = data['uid']).count() == 0:
				
				
				userprofile = Profile(realname=register.get('realname',''),
					school = register.get('school',''),
					grade = register.get('grade',''),
					major = register.get('major',''),
					mphone = register.get('mphone',''),
					phone = register.get('phone',''),
					user_type = 0,
					)

				cuser = User.objects.create_user(username=data['uid'],password=data['psd'],email='example@example.com')
				cuser.save()

				userprofile.user = cuser
				userprofile.save()

				
				'''begin handle course data'''
				error = Stu_elective_handler.handleElectiveCourse(cookie_value,cuser)
				_login(request)
				return HttpResponse(error)
				
			else:
				cuser = User.objects.get(username=data['uid'])
				cuser.set_password(data['psd'])
				try:
					profile = Profile.objects.get(user=cuser.id)
				except:
					profile = Profile(realname=register.get('realname',''),
						school = register.get('school',''),
						grade = register.get('grade',''),
						major = register.get('major',''),
						mphone = register.get('mphone',''),
						phone = register.get('phone',''),
						user_type = 0,
					)
				profile.realname = register.get('realname','')
				profile.school = register.get('school','')
				profile.grade = register.get('grade','')
				profile.grade = mphone = register.get('mphone','')
				profile.user_type = 0
				profile.phone = register.get('phone','')
				profile.save()
				
				course_set = cuser.course_set.filter(termnumber = getTermNumber())

				for ccourse in course_set:
					ccourse.user.remove(cuser)
					ccourse.save()
				cuser.save()
				error = Stu_elective_handler.handleElectiveCourse(cookie_value,cuser)
				_login(request)
				return HttpResponse(error)
		else:
			return HttpResponse(mlogin)
	return HttpResponse('-1')

@require_http_methods(['POST'])
def login_portal(request):
	def _login(request):
		user = authenticate(username = request.POST.get('username',''),\
			password = request.POST.get('passwd',''))
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return HttpResponse('0')
			else:
				return HttpResponse('-1')
		return HttpResponse('-202')
	
	url_exit_portal = 'http://portal.pku.edu.cn//infoPortal/logout.do'
	url_login_portal = 'http://portal.pku.edu.cn:80/infoPortal/login.do'
	url_course_doc = 'http://portal.pku.edu.cn/infoPortal/appmanager/myPortal/myDesktop?_nfpb=true&_pageLabel=myPortal_page_17'
	p_login_portal = re.compile(u'<B>(.*)</B>，欢迎登录信息门户')
	
	data = {}
	JSESSIONID = request.POST.get('sessionid','')
	headers={'Cookie':'JSESSIONID='+JSESSIONID}
	data['{actionForm.userid}'] = request.POST.get('username','')
	data['{actionForm.password}'] = request.POST.get('passwd','')
	data['{actionForm.validCode}'] = request.POST.get('valid','')
	
	
	
	if data['{actionForm.validCode}']==u'':
		_login(request)
	else:		
		url_values = urllib.urlencode(data)
		cookieJar=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		req_login = urllib2.Request(url_login_portal,url_values,headers)
		response = opener.open(req_login)
		    
		match_login = p_login_portal.search(response.read().decode('utf8'))
		if match_login:
			register = {}
			register['realname'] = match_login.group(1)
			'''Get Course Doc'''
			req = urllib2.Request(url_course_doc)
			response = opener.open(req)
			doc_xkqk = response.read()
			response.close()
			'''退出'''
			req = urllib2.Request(url_exit_portal)
			response = opener.open(req)
			response.close()
			
			'''if user does not exists yet'''
			if User.objects.filter(username = data['{actionForm.userid}']).count() == 0:
				
				
				userprofile = Profile(realname=register.get('realname',''),
					school = register.get('school',''),
					grade = register.get('grade',''),
					major = register.get('major',''),
					mphone = register.get('mphone',''),
					phone = register.get('phone',''),
					user_type = 1,
					)

				cuser = User.objects.create_user(username=data['{actionForm.userid}'],password=data['{actionForm.password}'],email='example@example.com')
				cuser.save()

				userprofile.user = cuser
				userprofile.save()

				
				'''begin handle course data'''
				error = MasterStu_handler.parse_course_page(doc_xkqk,cuser)
				_login(request)
				return HttpResponse(error)
				
			else:
				cuser = User.objects.get(username=data['{actionForm.userid}'])
				cuser.set_password(data['{actionForm.password}'])
				try:
					profile = Profile.objects.get(user=cuser.id)
				except:
					profile = Profile(realname=register.get('realname',''),
						school = register.get('school',''),
						grade = register.get('grade',''),
						major = register.get('major',''),
						mphone = register.get('mphone',''),
						phone = register.get('phone',''),
						user_type = 1,
					)
				profile.realname = register.get('realname','')
				profile.school = register.get('school','')
				profile.grade = register.get('grade','')
				profile.grade = mphone = register.get('mphone','')
				profile.user_type = 1
				profile.phone = register.get('phone','')
				profile.save()
				
				course_set = cuser.course_set.filter(termnumber = getTermNumber())

				for ccourse in course_set:
					ccourse.user.remove(cuser)
					ccourse.save()
				cuser.save()
				error = MasterStu_handler.parse_course_page(doc_xkqk,cuser)
				_login(request)
				return HttpResponse(error)
		else:
			return HttpResponse('-3')
	return HttpResponse('-1')


def index(request):
	cookie=cookielib.CookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response=opener.open(urlimg)
	t=response.read()
	PHPSESSID=''
	for item in cookie:
	    if item.name=='PHPSESSID':
		    PHPSESSID=item.value
	img=open(MEDIA_ROOT+"dean"+".gif","wb")
	img.write(t)
	img.close()
	context={'sid':PHPSESSID}
	
	'''setup for portal testing'''
	url_portal_img = 'http://portal.pku.edu.cn/infoPortal/DrawServlet?Rand=5052.215403411537'
	cookieJar=cookielib.CookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	JSESSIONID=''
	response=opener.open(url_portal_img)
	img=response.read()
	
	imgfile=open(MEDIA_ROOT+"protal.gif","wb")
	imgfile.write(img)
	imgfile.close()
	for item in cookieJar:
	    if item.name=='JSESSIONID':
		    JSESSIONID=item.value
		    
	context['portal_sid'] = JSESSIONID
	

	url_elective_img = "http://elective.pku.edu.cn/elective2008/DrawServlet?Rand=1898.0822409503162"
	cookieJar=cookielib.CookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	JSESSIONID=''
	response=opener.open(url_elective_img)
	img=response.read()
	
	imgfile=open(MEDIA_ROOT+"elective.gif","w")
	imgfile.write(img)
	imgfile.close()
	for item in cookieJar:
	    if item.name=='JSESSIONID':
		    JSESSIONID=item.value
		    
	context['elective_id'] = JSESSIONID
	return render_to_response("index.html",context)

def login_required_message(request):
	return HttpResponse('-10')


     
