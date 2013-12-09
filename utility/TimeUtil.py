# -*- coding:UTF-8 -*-
import urllib,urllib2
import re
urlxl = "http://dean.pku.edu.cn/classroom/pkuclassroom.php"

pWeekNumber = re.compile(u'校历第([0-9]+)周')


def getWeekNumber():
    request = urllib2.Request(urlxl)
    response = urllib2.urlopen(request).read().decode('GBK')
    weekMatch = pWeekNumber.search(response)
    
    if weekMatch:
        return int(weekMatch.group(1))
    else:
        return -1
    
def getTermNumber():
    return 4
