#!/usr/bin/python

import urllib2
url = "http://www.pkucada.org:8082/Server/manage/update"
req = urllib2.Request(url)
res = urllib2.urlopen(req)
res.close()
print 'update Classroom Data'

