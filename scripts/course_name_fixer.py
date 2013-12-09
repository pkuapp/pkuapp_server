#! python
#coding=utf-8
import _mysql
import MySQLdb
import string
import re
import time
import csv

cb=MySQLdb.connect("localhost","root","cada2009",charset="utf8")
c = cb.cursor()

f = open('result.csv','r')
T = list()
name_reader = csv.reader(f)
for row in name_reader:
    T.append([row[1],row[2],row[0]])

c.executemany("update pkuapp.server_course set cname=%s,ename=%s where courseid=%s and termnumber=4",T)
cb.commit()

f = open('result-fixed.csv','r')
T = list()
name_reader = csv.reader(f)
for row in name_reader:
    T.append([row[1],row[2],row[0]])

c.executemany("update pkuapp.server_course set cname=%s,ename=%s where courseid=%s and termnumber=4",T)
cb.commit()


