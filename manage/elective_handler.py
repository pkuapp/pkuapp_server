#! python
# -*- coding:UTF-8 -*-
import urllib
import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup,SoupStrainer,Tag
from Server.models import course,place
from Server.utility.TimeUtil import getTermNumber

term = getTermNumber()
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
urlCourseDo = "http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/getCurriculmByForm.do"

urlTongXuanKe2 = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/queryCurriculum.jsp?netui_row=syllabusListGrid%3B50'
urlTongXuanKe3 = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/queryCurriculum.jsp?netui_row=syllabusListGrid%3B100'

urlCoursePagei = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/queryCurriculum.jsp?netui_row=syllabusListGrid%3B'

list_day = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']

re_time=re.compile(u'([每|单|双]周)周(.?)([0-9]+)~([0-9]+)')
re_TotalPage = re.compile(u'of ([0-9]+)')
course_type_list = ['education_plan_bk','speciality','politics','english','gym','trans_choice','pub_choice','liberal_computer','pt']
re_TotalPage = re.compile(u'of ([0-9]+)')

def run_elective_course_update(cookie_value):
	"登陆后将cookie_value传入"
	return_m = ''
	
	data = {}
	for ctype in course_type_list:
		data['wlw-radio_button_group_key:{actionForm.courseSettingType}'] = ctype
		values = urllib.urlencode(data)
		request = urllib2.Request(urlCourseDo,values)
		request.add_header('Cookie',cookie_value)
		response = urllib2.urlopen(request)
		doc = response.read()
		# return doc
		response.close()
		match_page = re_TotalPage.search(doc)
		return_m += handle_course_list(doc,ctype)
		# return match_page
		if match_page:
			for i in xrange(1,int(match_page.group(1))+1):
				urlPage = urlCoursePagei + str(i*50)
				request = urllib2.Request(urlPage,values)
				request.add_header('Cookie',cookie_value)
				response = urllib2.urlopen(request)
				doc = response.read()
				response.close()
				return_m += handle_course_list(doc,ctype)
	
	"""data2 = {}
	data2['wlw-radio_button_group_key:{actionForm.courseSettingType}'] = 'trans_choice'
	"参看elective的选课计划的网页,此处代表抓通选课"
	Txkvalues = urllib.urlencode(data2)
	request = urllib2.Request(urlTongXuanKe,Txkvalues)
	request.add_header('Cookie',cookie_value)

	response = urllib2.urlopen(request)

	#return_m += handle_course_list(response.read(),'tx')
	response.close()
	
	request = urllib2.Request(urlTongXuanKe2)
	request.add_header('Cookie',cookie_value)
	response = urllib2.urlopen(request)
	#return_m += handle_course_list(response.read(),'tx')
	response.close()
	
	request = urllib2.Request(urlTongXuanKe3)
	request.add_header('Cookie',cookie_value)
	response = urllib2.urlopen(request)
	#return_m += handle_course_list(response.read(),'tx')
	response.close()
	
	data3 = {}
	data3['wlw-radio_button_group_key:{actionForm.courseSettingType}'] = 'pub_choice'
	"以下开始抓公选课"
	Gxkvalues = urllib.urlencode(data3)
	
	request = urllib2.Request(urlTongXuanKe,Gxkvalues)
	request.add_header('Cookie',cookie_value)
	response = urllib2.urlopen(request)

	#return_m += handle_course_list(response.read())
	response.close()
	
	request = urllib2.Request(urlTongXuanKe2)
	request.add_header('Cookie',cookie_value)
	response = urllib2.urlopen(request)
	#return_m += handle_course_list(response.read())
	response.close()
	
	
	'PE Course'
	data4 = {}
	data4['wlw-radio_button_group_key:{actionForm.courseSettingType}'] = 'gym'
	PEvalues = urllib.urlencode(data4)
	request = urllib2.Request(urlTongXuanKe,PEvalues)
	request.add_header('Cookie',cookie_value)
	response = urllib2.urlopen(request)
	return_m += handle_course_list(response.read(),'PE')
	response.close()
	for i in xrange(1,4):
		urlPE = urlCoursePagei + str(i*50)
		
		
		
		request = urllib2.Request(urlPE,PEvalues)
		request.add_header('Cookie',cookie_value)
		response = urllib2.urlopen(request)
		return_m += handle_course_list(response.read(),'PE')
		response.close()
		"""
	return return_m
def match_time(string):
	def set_daytime(m,context):
        	for i,dayx in enumerate(list_day):
			if m.group(2) == dayx:
				if m.group(1) != u'每周':
					context['day'+str(i+1)] = m.group(3)+'-'+m.group(4) + m.group(1)
				else:
					context['day'+str(i+1)] = m.group(3)+'-'+m.group(4)
	context = {}
	for i in xrange(7):
		context['day'+str(i+1)]=0
	
     	m1 = re_time.search(string)
     	if m1:
     		
		m2 = re_time.search(string[m1.end():])
		set_daytime(m1,context)
		if m2:
        		#print m2.group(i)
        		set_daytime(m2,context)
        	
        		
	for i in xrange(7):
		if context['day'+str(i+1)]:
			context['timeKey'] = context.get('timeKey','') + str(i) + context['day'+str(i+1)]

        return context
        
 
def save_txcourse(context):        
	error = ''
	try:
		keyid = context['courseid'] + context.get('timeKey','') + context['teachername']
		try:
			ccourse = course.objects.get(courseid=context['courseid'],termnumber=term)
		except:
			ccourse = course.objects.get(keyid = keyid,termnumber=term)
		ccourse.txType = context['txType']
		ccourse.save()
		pass
		
		
	except:
		error += 'keyid:'+keyid+'##'
		return error
	return save_course(context)

def save_course(context):
	error = ''
	try:
		keyid = context['courseid'] + context.get('timeKey','') + context['teachername']
		try:
			ccourse = course.objects.get(courseid=context['courseid'],termnumber=term)
		except:
			ccourse = course.objects.get(keyid = keyid,termnumber=term)
		ccourse.rawplace = context.get('placename','')
		ccourse.save()
		try:
			
			pass
			try:
				placeKeyid = str(context.get('location','')) + context.get('interid','')
				if placeKeyid != '':
					cplace = place.objects.get(keyid=placeKeyid)
					ccourse.place = cplace
				ccourse.save()
			except:
				error += 'place:'+placeKeyid +'\n'
		except:
			error += 'keyid:'+keyid+'\n'
			return error
	except:
		error += 'keyid:'+keyid+'\n'
		return error
		
	return ''
	
def save_pecourse(context):
	error = ''
	keyid = context['courseid'] + context.get('timeKey','') + context['teachername']
	try:
		try:
			ccourse = course.objects.get(courseid=context['courseid'],termnumber=term)
		except:
			
			ccourse = course.objects.get(keyid = keyid,termnumber=term)
		ccourse.rawplace = context.get('placename','')
		ccourse.save()
		try:
			pass
		except:
			error += 'keyid:'+keyid+'\n'
			return error
	except:
		error += 'keyid:'+keyid+'\n'
		return error
	return ''
	

def handle_course_list(string,course_type='default'):

        strainer=SoupStrainer('table',width="100%")
        soup_classroom=BeautifulSoup(string,parseOnlyThese=strainer)
        error = ''
        for tr in soup_classroom.table:
                    if type(tr)!=Tag or tr.get('class')=='datagrid-header':
                        continue
                    contents = tr.contents
                    if len(contents) > 1 and tr.td.get('colspan')!='12':
                    	    	context={'courseid':contents[1].contents[0].contents[0].getText(),
				    'name':contents[3].contents[0].getText(),
				    'timeandplace':contents[19].contents[0].getText(),
				    'txType':contents[5].contents[0].getText(),
				    'teachername':contents[9].contents[0].getText(),
				}
	
				time_context = match_time(context['timeandplace'])
				place_context = place.dictFromPlaceString(context['timeandplace'])
				context.update(time_context)
				if course_type == 'gym':
					place_context = {'placename':contents[21].contents[0].getText()}

					context.update(place_context)
					error += save_pecourse(context)
				elif course_type == 'english':
					if place_context is None:
						tempstring = contents[21].contents[0].getText()
						place_context = place.dictFromPlaceString(tempstring)
					context.update(place_context)
					error += save_pecourse(context)
				else:
					if place_context:
						context.update(place_context)
					if course_type == 'trans_choice':
						error += save_txcourse(context)
					else:
						error += save_course(context)
	return error
	
	

