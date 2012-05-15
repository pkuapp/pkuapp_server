#! python
import urllib2
url = "http://127.0.0.1:8082/Server/manage/update"
req = urllib2.Request(url)
res = urllib2.urlopen(req)
res.close()
a = rawinput()
print 'update Classroom Data'

