#! python
import _mysql
import MySQLdb
import string
import re
import time
p = re.compile(u"""(?<=II)((([^\u4e00-\ufad9()])*([ ]*\([^(]*\)[ ]*){0,}[ ]*$))""")

p3 = re.compile(u'''([a-zA-Z0-9《》：、\－\u4e00-\ufad9（）\(\)]+) *([^ ]*) *([^()]*) *([^ ]*|\(.*\))$''')

p2 = re.compile(u'[()z-zA-Z]')
db=MySQLdb.connect("localhost","root","cada2009",charset="utf8")
cb=MySQLdb.connect("localhost","root","cada2009",charset="utf8")
c = cb.cursor()
query = db.query("""SELECT * FROM `mobile`.`server_course` where termnumber=2""")
results = db.use_result()
num_rows = 5577

print p3.search(u'高等统计选讲 I Selected Topics on Advanced Statistics I').group(1)
print p3.search(u'阅读与写作（中级下） Reading and Writing Chinese II (intermediate level)').group(4)
T = list()
f = open('result.csv','w')
for i in xrange(num_rows//1000+1):
                
                rows = results.fetch_row(1000)
                for crow in rows:
   
                     setid = crow[0]
                     name = crow[4]
                     courseid = crow[2]
                     m = p3.match(name)
                     cname = None
                     ename = None
                     if m is not None:
                              end1 = m.group(2)
                              end2 = m.group(4)
                              if end1 == end2:
                                  cname = m.group(1) + ' '+ end1
                                  ename = m.group(3) + ' ' + end2
                              else:
                                  cname = m.group(1)
                                  ename = end1 + ' '+ m.group(3) + ' '+end2
                              T.append((cname.strip(),ename.strip(),setid))
                              a = u'%s,%s,%s\n' % (courseid,cname,ename)
                              f.write(a.encode('utf8'))
 #                             c.execute("""UPDATE mobile.server_course set cname=%s,ename=%s where id= %s """,)
                              
##                              if p2.search(a):
##                                   print a
                              #print m.group(0)
                     else:
                         print courseid,name
c.executemany("""UPDATE mobile.server_course set cname=%s,ename=%s where id= %s """,T)
cb.commit()
f.close()

                
                         #print name
                     #if setid%100 == 0:
                     #        print setid
                     #if raw_place:
                     #        raw_place = raw_place.replace('&nbsp;','').replace('\n','').replace('\t','')
                     #        print raw_place
                             #c.execute("""UPDATE mobile.server_course set rawplace=%s where id= %s """,(raw_place,setid,))
                     #cb.commit()
                    


        


