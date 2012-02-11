# -*- coding:UTF-8 -*-

from types import *
from BeautifulSoup import *
import urllib
import urllib2
import re
from Server.models import course,School
from django.http import HttpResponse

urlCoursePlanData = r"http://dean.pku.edu.cn/jiaoxuejihua/kcb.php"
urlSchoolList = r"http://dean.pku.edu.cn/jiaoxuejihua/kcbxs.php?ll=1"

'''学期数从10-11学年第二学期开始为0'''

def run_update_dean_course(request):
	xq = request.GET.get('xq',None)
	xq = int(xq)
	if xq is None:
		return HttpResponse('-101')
	
	xq_string = str((xq + 1)  % 2 + 1)
	xn_string = str(10 + (xq + 1) / 2) + "-" + str(11 + (xq + 1)/ 2)
	
	urlPubElectiveCourse = r"http://dean.pku.edu.cn/jiaoxuejihua/kcbgx.php3?xn=" +\
	xn_string + "&xq=" +xq_string
	urlPubReqCourse = r"http://dean.pku.edu.cn/jiaoxuejihua/kcbbx.php?xn=" +\
	xn_string + "&xq=" +xq_string
	urlGeneralCourse = r"http://dean.pku.edu.cn/jiaoxuejihua/kcbtx.php?xn=" +\
	xn_string + "&xq=" +xq_string
	meg = ''
	requestPEC = urllib2.Request(urlPubElectiveCourse)
	responseDoc = urllib2.urlopen(requestPEC)
	responseString = responseDoc.read()
	meg +=_handleCourseFromTable2(responseString,xq)
	
	requestPRC = urllib2.Request(urlPubReqCourse)
	responseString = urllib2.urlopen(requestPRC)
	meg += _handleCourseFromTable(responseString,xq)
	
	requestGC = urllib2.Request(urlGeneralCourse)
	responseString = urllib2.urlopen(requestGC).read()
	meg += _handleCourseFromTable2(responseString,xq)
	
	
	"getCourseofSchool"
	urlSchoolList = r"http://dean.pku.edu.cn/jiaoxuejihua/kcbxs.php?ll=1"
	
	requestSchoolList = urllib2.Request(urlSchoolList)
	responseDoc = urllib2.urlopen(requestSchoolList)
	responseString = responseDoc.read()
	listschool = _getSchoolList(responseString)
	
	for SchoolCode in listschool:
		
		queryset = School.objects.filter(code=SchoolCode[0])
		if queryset.count() == 0:
			cschool = School(code = SchoolCode[0],name = SchoolCode[1],ename = SchoolCode[2])
			cschool.save()
		meg += _handleCourseOfSchool(SchoolCode[0],xq)
		
	return HttpResponse(meg)	

	
def _getSchoolList(string):
	contextlist = list()
	strainer = SoupStrainer('table',border='1')
	soup_course = BeautifulSoup(string,parseOnlyThese=strainer,fromEncoding = 'GBK')
	tbody = soup_course.table
	for i,tr in enumerate(tbody):
		if i > 0:
			temp = (tr.contents[0].getText(),tr.contents[1].contents[0].getText(),tr.contents[2].contents[0].getText())
			contextlist.append(temp)

	return [(tr.contents[0].getText(),tr.contents[1].contents[0].getText(),tr.contents[2].contents[0].getText()) for i,tr in enumerate(tbody) if i >0]

def _handleCourseOfSchool(SchoolCode,xq):
	meg = ' '
	def __stringCourse(SchoolCode):
		data = {}
		data['xn'] = str(10 + (xq + 1) / 2) + "-" + str(11 + (xq + 1)/ 2)
		data['xq'] = str((xq + 1)  % 2 + 1)
		data['xs'] = SchoolCode
		data['zy'] = "%"
		data['nj'] = "%"
		postData = urllib.urlencode(data)
		request = urllib2.Request(urlCoursePlanData,postData)
		responseDoc = urllib2.urlopen(request)
		responseString = responseDoc.read()
		return responseString
	
	string = __stringCourse(SchoolCode)
	return _handleCourseFromTable(string,xq,SchoolCode = SchoolCode)
	
def _handleCourseFromTable(string,xq,SchoolCode = ''):
	meg = ' '
	def __ListDaydataFromString(context_list):
			ccourse = course()			
			return [ccourse.daydataFromDayString(context_list[11+i]) for i in range(7)]
	strainer = SoupStrainer('table',border='1')
	soup_course = BeautifulSoup(string,parseOnlyThese=strainer,fromEncoding = 'GBK')
	tbody = soup_course.table
	if tbody is None:
		return '-1'
	for i,tr in enumerate(tbody):
	    if tr != None:
		if i > 0:
			    context_list = list()
			    for td in tr.contents:
				    if td.font != None:
					    context_list.append(td.font.getText().replace(u'&nbsp;','').strip(u' ')) 
					
				    elif td.a != None:    
					    context_list.append(td.a.getText().replace(u'&nbsp;','').strip(u' '))
				    else:
					    temp = td.getText().replace(u'&nbsp;','').strip(u' ')
					    context_list.append(temp)
			
			    
			    ckeyid = context_list[0]
			    for i in range(7):
			    	    tempStr = context_list[i+11].strip()
			    	    if tempStr:
			    	    	    ckeyid +=str(i) + tempStr
			    ckeyid = ckeyid.strip()
			    ckeyid += context_list[7]
			    queryset = course.objects.filter(keyid=ckeyid,termnumber=xq)
			    if queryset.count() > 0:
				   ccourse = queryset.get(keyid=ckeyid)
				   ccourse.SchoolCode = SchoolCode
				   ccourse.CourseType = context_list[3]
				   ccourse.name = context_list[1]
				   ccourse.save()
				   
			    else:
				   dayx = __ListDaydataFromString(context_list)
				   
				   ccourse = course(termnumber=xq,keyid=ckeyid,courseid=context_list[0],classnum=context_list[2],\
				   	   name=context_list[1],rawplace=None,time_test=None,credit=context_list[4],\
				   	   time=context_list[10],day1=dayx[0],day2=dayx[1],day3=dayx[2],day4=dayx[3],\
				   	   day5=dayx[4],day6=dayx[5],day7=dayx[6],teachername=context_list[7],\
				   	   SchoolCode = SchoolCode,Coursetype = context_list[3],course_category=0)
				   ccourse.save()
				  
      
	return meg
	
def _handleCourseFromTable2(string,xq,SchoolCode = None):
	meg = ' '
	def __ListDaydataFromString(context_list):
			ccourse = course()			
			return [ccourse.daydataFromDayString(context_list[10+i]) for i in range(7)]
	strainer=SoupStrainer('table',border='1')
	soup_course=BeautifulSoup(string,parseOnlyThese=strainer,fromEncoding="GBK")
	tbody=soup_course.table
	if tbody is None:
		return '-1'
	for i,tr in enumerate(tbody):
	    if tr != None:
		if i > 0:
			    context_list = list()
			    for td in tr.contents:
				    if td.font != None:
					    context_list.append(td.font.getText().replace(u'&nbsp;','').strip(u' ')) 
					
				    elif td.a != None:    
					    context_list.append(td.a.getText().replace(u'&nbsp;','').strip(u' '))
				    else:
					    temp = td.getText().replace(u'&nbsp;','').strip(u' ')
					    context_list.append(temp)
			
			    
			    ckeyid = context_list[0]
			    for i in range(7):
			    	    tempStr = context_list[i+10].strip()
			    	    if tempStr:
			    	    	    ckeyid += str(i) + tempStr
			    ckeyid = ckeyid.strip()
			    ckeyid += context_list[6]
			    queryset = course.objects.filter(keyid=ckeyid,termnumber=xq)
			    if queryset.count() > 0:
				   ccourse = queryset.get(keyid=ckeyid)
				   ccourse.SchoolCode = SchoolCode
				   ccourse.CourseType = context_list[3]
				   ccourse.name = context_list[1]

				   ccourse.save()
				   
			    else:
				   dayx = __ListDaydataFromString(context_list)
				   
				   ccourse = course(termnumber=xq,keyid=ckeyid,courseid=context_list[0],classnum=0,\
				   	   name=context_list[1],rawplace=None,time_test=None,credit=context_list[3],\
				   	   time=context_list[9],day1=dayx[0],day2=dayx[1],day3=dayx[2],day4=dayx[3],\
				   	   day5=dayx[4],day6=dayx[5],day7=dayx[6],teachername=context_list[6],\
				   	   SchoolCode = SchoolCode,Coursetype = context_list[2],course_category=0)
				   ccourse.save()
				  
      
	return meg
