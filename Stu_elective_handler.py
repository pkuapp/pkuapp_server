# coding:utf-8
import urllib
import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup,SoupStrainer,Tag
from Server.models import course,place
from Server.utility.TimeUtil import getTermNumber

term = getTermNumber()

def match_time(string):
    re_time=re.compile(u'([每|单|双]周)周(.?)([0-9]+)~([0-9]+)')
    list_day = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']

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

def parse_course_page(string,cuser):

    strainer=SoupStrainer('table',width="100%")
    soup_classroom=BeautifulSoup(string,parseOnlyThese=strainer)
    error = u'0'
    if soup_classroom.table is None:
        return string
    tbody = soup_classroom.table
    for tr in tbody:
     
        
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
            error += savecourse(context,cuser)
        print context
    return error

def savecourse(context,cuser):
    courseid = course.objects.filter(name__contains=context['name'])[0].courseid
    error = u''
    try:
        keyid = courseid + context.get('timeKey','') + context['teachername']
        try:
            ccourse = course.objects.get(courseid=context['courseid'],termnumber=term)
        except:
            ccourse = course.objects.get(keyid = keyid,termnumber=term)

        ccourse.user.add(cuser)
        ccourse.save()
    except:
        error += 'name:'+context['name']+'#'
    return error
