import urllib
import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup,SoupStrainer,Tag
from Server.models import course,place
from Server.utility.TimeUtil import getTermNumber

term = getTermNumber()

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

def parse_course_page(doc_xkqk,cuser):

        strainer=SoupStrainer('table',width="100%")
        soup_classroom=BeautifulSoup(string,parseOnlyThese=strainer)
        error = ''
        for tr in soup_classroom.table:
                    if type(tr)!=Tag or tr.get('class')=='datagrid-header':
                        continue
                    contents = tr.contents
                    if len(contents) > 1 and tr.td.get('colspan')!='12':
                    	    	context={
				    'name':contents[1].contents[0].getText(),
				    'timeandplace':contents[15].contents[0].getText(),
				    'teachername':contents[9].contents[0].getText(),
				}
				time_context = match_time(context['timeandplace'])
				context.update(time_context)
				error += savecourse(context)
	return error

def savecourse(context):
    courseid = course.objects.filter(name=context['name'])[0].courseid
    error = ''
    try:
        keyid = courseid + context.get('timeKey','') + context['teachername']
        try:
            ccourse = course.objects.get(courseid=context['courseid'],termnumber=term)
        except:
            ccourse = course.objects.get(keyid = keyid,termnumber=term)
        ccourse.user.add(cuser)
        ccourse.save()
    except:
        error += 'keyid:'+keyid+'##'
    return error
