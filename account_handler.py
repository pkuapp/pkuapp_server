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
context_re={'username':re.compile(u'学号：([^<]+)'),
            'realname':re.compile(u'姓名：([^<]+)'),
            'email':re.compile(u'Email：[^%]+?value=([^@]+?@[^ ]+)[^%]+?以下'),
            'school':re.compile(u'院系：([^<]+)'),
            'major':re.compile(u'专业：([^<]+)'),
            'grade':re.compile(u'年级：([^<]+)'),
            'mphone':re.compile(u"""手机号码：[^%]+?value=([^ ]+)[^%]+?固"""),
            'phone':re.compile(u"""固定电话：[^%]+?value=([^ ]+)[^%]+?Email"""),                   
            }
       
def dict_deanprofile(target):
	#ptable=re.compile(u'\<table width[^~]+(\</table\>)')
	#table=re.search(ptable,target).group(0)
	context={}
	for k in context_re:
            m=re.search(context_re[k],target)
            if m:
            	    context[k]=m.group(1).strip("""'""")
        return context

def dict_course(lists):
	daylist=list()
	for i,raw_string in enumerate(lists[11:18]):
		daydata = course.daydataFromDayString(raw_string)
		daylist.append(daydata)
	keyid = lists[0]
	'''this part is to calc this unique keyid of course'''
	for i in range(7):
		tempStr = lists[11+i].strip()
		if tempStr:
			keyid += str(i) + tempStr
	
	keyid = keyid.strip() + lists[7].strip()
	
	rawplace = lists[18]+lists[19]
	
	rawplace = rawplace.replace('\n','').replace('\t','').replace('&nbsp;','')
	
	context={'keyid':keyid,
		'courseid':lists[0],
		'name':lists[1],
		'classnum':lists[2],
		'credit':lists[4],
		'time':lists[10],
		'rawplace':rawplace,
		'teachername':lists[7].strip(),
		'time_test':lists[20]
	}
	for i in xrange(7):
		context['day'+str(i+1)] = daylist[i]
	return context
        
def handle_course(string,user):
        strainer = SoupStrainer('table',border='1')
        soup_course = BeautifulSoup(string,parseOnlyThese=strainer)
        tbody = soup_course.table
        if tbody is None:
        	return '0'
        for i,tr in enumerate(tbody):
        	if i>0:
        		lists = list()
        		
			for td in tr:
				if type(td) == Tag:
					x = td.contents[0].__str__().decode('utf8').replace('&nbsp;','')
					
					lists.append(x)
			context = dict_course(lists)
			ckeyid = context['keyid']
        		queryset = course.objects.filter(keyid=ckeyid,termnumber=getTermNumber(),course_category = 0)
        		if queryset.count() == 0:
				thecourse = course(termnumber=getTermNumber(),keyid=context['keyid'],courseid=context['courseid'],classnum=context['classnum'],name=context['name'],rawplace=context['rawplace'],time_test=context['time_test'],credit=context['credit'],time=context['time'],day1=context['day1'],day2=context['day2'],day3=context['day3'],day4=context['day4'],day5=context['day5'],day6=context['day6'],day7=context['day7'],teachername=context['teachername'],course_category = 0)
				thecourse.save()
				thecourse.user.add(user)
				thecourse.save()
        		else:
        			
        			thecourse = course.objects.get(keyid=ckeyid,termnumber=getTermNumber(),course_category = 0)
        			thecourse.classnum = context['classnum']
        			thecourse.rawplace = context['rawplace']
        			thecourse.time_test = context['time_test']
        			thecourse.user.add(user)
        			thecourse.save()
			contextplace = place.dictFromPlaceString(context['rawplace'])
			
			if contextplace != None:
				placekey=str(contextplace['location'])+contextplace['interid']
				if place.objects.filter(keyid=placekey).count()>0:
					thepalce=place.objects.get(keyid=placekey)
					thecourse.place=thepalce
					thecourse.save()
        return '0'

