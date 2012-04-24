# coding:utf-8
import urllib
import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup,SoupStrainer,Tag
from Server.models import course,place
from Server.utility.TimeUtil import getTermNumber
term = getTermNumber()
def handleElectiveCourse(cookie_value,cuser):
    url_do = "http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/electiveWork/showResults.do"
    url_resulti = "http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/electiveWork/showResults.jsp?netui_row=electedCourseListGrid%3B"
    _req = urllib2.Request(url_do)
    
    _req.add_header('Cookie',cookie_value)
    response = urllib2.urlopen(_req)
    doc_xkqk = response.read().decode('utf8')
    response.close()
    re_TotalPage = re.compile(u'of ([0-9]+)')
    match_page = re_TotalPage.search(doc_xkqk)
    if not match_page:
        return 'courses not found'
    for i in xrange(1,int(match_page.group(1))+1):

        url = url_resulti + str(i*5)
        _req = urllib2.Request(url)
        _req.add_header('Cookie',cookie_value)
        response = urllib2.urlopen(_req)
        string = response.read()
        response.close()
        parse_course_page(string,cuser)
    return '0'

def match_location_context(string):

    list_building=[u"一教",u"二教",u"三教",u"四教",u"文史",\

        u"电教",u"哲学",u"物理",u"地学",u"技物",\

        u"外文",u"体教",u"数学",u"化学",u"电子",\

        u"理教",u"电教听力",u"国关",u"政管",u"光华",\

        u"理科2#"]

    list_re=[re.compile(x+u'([a-zA-Z0-9]+)') for x in list_building]

    if string=='':
        return None 

        for i in range(21):

        #px=getattr(stringmap,'p'+str(i+1)
             m2 = re.search(list_re[i],string)
        if m2:
            return {'location':i+1,
                'name':m2.group(0),
                'interid':m2.group(1)
            }    
    return None

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

    def set_daytime_with_tuple(time,context):
        for i,dayx in enumerate(list_day):
            if time[1] == dayx:
                if time[0] != u'每周':
                    context['day'+str(i+1)] = time[2]+'-'+ time[3] + time[0]
                else:
                    context['day'+str(i+1)] = time[2] +'-'+time[3]
    context = {}
    for i in xrange(7):
        context['day'+str(i+1)]=''
   
    for time in re_time.findall(string):
        set_daytime_with_tuple(time,context)
  
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
            if contents[19].contents[0].getText() == u'未选上' :
                continue
            if contents[19].contents[0].getText() == u'已退课' :
                continue
            context={
            'name':contents[1].contents[0].getText().strip().replace('&nbsp;',''),
            'timeandplace':contents[15].contents[0].getText(),
            'teachername':contents[9].contents[0].getText(),
            'credit':contents[5].contents[0].getText(),
            }
            
            time_context = match_time(context['timeandplace'])
            context.update(time_context)
            savecourse(context,cuser)
    return error

def savecourse(context,cuser):
    
    courseid = course.objects.filter(name__contains=context['name'],termnumber=getTermNumber(),teachername__contains=context['teachername'])[0].courseid
    error = u''
    keyid = courseid + context.get('timeKey','') + context['teachername']
    place_context = match_location_context(context['timeandplace'])
    try:
        ccourse = course.objects.get(keyid = keyid,termnumber=term)
    except:
        context.pop('timeandplace')
        context.pop('timeKey')
        for x in xrange(7):
                        context['day'+str(x+1)] = course.daydataFromDayString(context['day'+str(x+1)])
        ccourse = course(keyid=keyid,termnumber=getTermNumber(),course_category=0,**context)
        ccourse.save()
        if place_context:
               
                   ccourse.rawplace = place_context['name']
                   ccourse.save()
            
    #       try:
    #           ccourse = course.objects.get(courseid=context['courseid'],termnumber=term,teachername__contains=context['teachername'])
    #       except:
    #           pass
    ccourse.user.add(cuser)
    ccourse.save()
    if place_context:
        ccourse.rawplace = place_context['name']
        ccourse.save()
    return error
