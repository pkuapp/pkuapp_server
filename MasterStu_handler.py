#! python
# -*- coding:UTF-8 -*-

from types import *
from BeautifulSoup import *
import re
from django.contrib.auth.models import User
from Server.models import *
from Server.utility.TimeUtil import getTermNumber

psingle=re.compile(u'单周')
pdouble=re.compile(u'双周')
pmath=re.compile(u'[0-9]+')

#'cause portal and dean may differ from time, so it's better to maintain
#their pattern and functions in their own scripts.

context_re={'username':re.compile(u'学号：([^<]+)'),
            'realname':re.compile(u'姓名：([^<]+)'),
            'email':re.compile(u'Email：[^%]+?value=([^@]+?@[^ ]+)[^%]+?以下'),
            'school':re.compile(u'院系：([^<]+)'),
            'major':re.compile(u'专业：([^<]+)'),
            'grade':re.compile(u'年级：([^<]+)'),
            'mphone':re.compile(u"""手机号码：[^%]+?value=([^ ]+)[^%]+?固"""),
            'phone':re.compile(u"""固定电话：[^%]+?value=([^ ]+)[^%]+?Email"""),                   
            }
list_day = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']

def match_time(daystring):
	def set_daytime(m,context):
        	for i,dayx in enumerate(list_day):
			if m.group(1) == dayx:
				context['day'+str(i+1)] = course.daydataFromDayString(m.group(2))
	context = {}
	for i in xrange(7):
		context['day'+str(i+1)]=0
	ptime = re.compile(u'周(.?)([0-9\-]*[每|单|双]*)')
	m1 = ptime.search(daystring)
	if m1:
		set_daytime(m1,context)

		m2 = ptime.search(daystring[m1.end():])
		if m2:
        		set_daytime(m2,context)
        return context
        
def parse_portal_profile(target):
	'this functio is imcomplete'
	#ptable=re.compile(u'\<table width[^~]+(\</table\>)')
	#table=re.search(ptable,target).group(0)
	context={}
	for k in context_re:
            m=re.search(context_re[k],target)
            if m:
            	    context[k]=m.group(1).strip("""'""")
        return context
"""def handle_classroom(string):
	tempfile=open('a.html','w')
	strainer=SoupStrainer('table',border="1")
	soup_classroom=BeautifulSoup(string,parseOnlyThese=strainer,\
		fromEncoding="GBK"
		)
	lists=list()
	

	for tr in soup_classroom.table.tbody:
	    if type(tr)==Tag:
	    	index=-4
	    	list_occupy=list()
		for i,td in enumerate(tr):
		   
		    if type(td)==Tag:
		    	
		    	index+=1
			if td.get('style')!=None:
				list_occupy.append(index)
		updatedata(list_occupy,namestring=tr.contents[0].contents[0].__str__(),\
		    	    roomtype=tr.contents[1].contents[0].__str__(),\
		    	   capacity=tr.contents[2].contents[0].__str__()
		    	    )
	return '0'"""

        
def parse_course_page(string,user):
	keywords = {}
	keywords['class'] = 'pkuportal-table-portlet'
	strainer = SoupStrainer('table',**keywords)
	soup_course = BeautifulSoup(string,parseOnlyThese=strainer)
	if soup_course.table is None:
		return '0'
	tbody = soup_course.table
	for i,tr in enumerate(tbody):
	    context = {}
	    if i < 4:
		continue
	    else:
		if type(tr) == Tag:
			context = {
				'courseid':tr.contents[1].getText(),
				'name':tr.contents[3].getText(),
				'classnum':tr.contents[5].getText(),
				'Coursetype':tr.contents[7].getText(),
				'time':tr.contents[13].getText(),
				'rawplace':tr.contents[15].getText()
				}
			context['keyid'] = context['courseid'] + context['classnum'] + context['rawplace'] + context['time']
			time_context = match_time(context['time'])
			if time_context:
				context.update(time_context)
			ckeyid = context['keyid']
			context['termnumber'] = getTermNumber()
			queryset = course.objects.filter(keyid=ckeyid,termnumber=getTermNumber(),course_category = 1)
			if queryset.count() == 0:
				thecourse = course(course_category = 1,**context)
				thecourse.save()
				thecourse.user.add(user)
				thecourse.save()
			else:
				
				thecourse = course.objects.filter(keyid=ckeyid,termnumber=getTermNumber(),course_category = 1)
				thecourse.update(**context)
				thecourse[0].user.add(user)
				thecourse[0].save()
				thecourse = thecourse[0]
			contextplace = place.dictFromPlaceString(context['rawplace'])
			
			if contextplace != None:
				placekey=str(contextplace['location'])+contextplace['interid']
				if place.objects.filter(keyid=placekey).count()>0:
					thepalce=place.objects.get(keyid=placekey)
					thecourse.place=thepalce
					thecourse.save()
	return '0'

