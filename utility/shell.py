#! python
# -*- coding:UTF-8 -*-
import sys
import urllib
import urllib2
import re
#from handle import handle_classroom,handle_course
from stringmap import getdeanprofile
url='http://dean.pku.edu.cn/classroom/classroom.php'
profile=open(r'd:\profile3.html')
string=profile.read()
target=string.decode('utf8')
ptable=re.compile(u'\<table width[^~]+(\</table\>)')
#table=re.search(ptable,target).group(0)


context_re={'keyid':re.compile(u'学号：([^<]+)'),
            'username':re.compile(u'姓名：([^<]+)'),
            'email':re.compile(u'Email：([^<]+)'),
            'school':re.compile(u'院系：([^<]+)'),
            'major':re.compile(u'专业：([^<]+)'),
            'grade':re.compile(u'年级：([^<]+)'),
            'mphone':re.compile(u"""手机号码：[^%]+?value='([^ ]+)'"""),
            'phone':re.compile(u"""固定电话：[^%]+?value='([^ ]+)'"""),                   
            }

data={}
data['zhouci']='7'
#for i in range(20,30):
data['jxl']='99'
data['zhouji']='99'
#req=urllib.urlencode(data)
#response=urllib2.urlopen(url,req)
#doc=response.read()
fileinput=open('D:\classroom.htm','r')
a=fileinput.read().__str__().decode("GBK").encode('utf-8')
type = sys.getfilesystemencoding()
fileinput2=open(r'D:\course.html')
b=fileinput2.read().decode('utf8')
#handle_classroom(a)
#handle_course(b,a)
##m=getdeanprofile(target)
##for x in m:
##    print x,m[x]
