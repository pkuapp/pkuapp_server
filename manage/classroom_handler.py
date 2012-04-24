#! python
# -*- coding:UTF-8 -*-
from Server.models import *

from BeautifulSoup import BeautifulSoup,SoupStrainer,Tag
from Server.env.env import *
from Server.env.urlmap import *
from django.contrib import auth
from django.http import HttpResponse
import urllib
import urllib2
from Server.utility.TimeUtil import getTermNumber,getWeekNumber


def updatedata(list_occupy,namestring,roomtype,capacity,number):
	message = ''
	if list_occupy:
		context = place.dictFromPlaceString(namestring)
		if context!= None:
			name = context['placename']
			location = context['location']
			rcapacity = capacity
			"设置daydata"
			for i in xrange(7):
				globals()['day'+str(i+1)] = placet.dayCodeFromWeekStateList(i+1,list_occupy)
			
			interid = context['interid']
			keyid = str(location)+interid
			message += classroom_save( name,location,interid,keyid,roomtype,rcapacity,day1,day2,day3,day4,day5,day6,day7,number)
		return message
	return message

def classroom_save(name,location,interid,keyid,roomtype,rcapacity,day1,day2,day3,day4,day5,day6,day7,number):
	message = ''
	if place.objects.filter(keyid=keyid).count()==0:
		cplace=place(name=name,location=location,interid=interid,keyid=keyid,roomtype=roomtype,rcapacity=rcapacity)
		cplace.save()
		message += 'add place' +keyid
	cplace=place.objects.get(keyid=keyid)
	if cplace.placet_set.filter(weeknumber=number).count()==0:
		
		cplacet=placet(day1=day1,day2=day2,day3=day3,day4=day4,day5=day5,day6=day6,day7=day7,weeknumber=number)
		cplacet.place = cplace
		cplacet.save()

		message += 'addtime'+cplace.name
	else:
		cplace.placet_set.filter(weeknumber=number).delete()
		
		cplacet = placet(day1=day1,day2=day2,day3=day3,day4=day4,day5=day5,day6=day6,day7=day7,weeknumber=number)
		cplacet.place = cplace
		cplacet.save()
		message += 'update time'+cplace.name
	
	return message
def handle_classroom(string,weeknumber):
	message =''
	strainer=SoupStrainer('table',border="1")
	soup_classroom=BeautifulSoup(string,parseOnlyThese=strainer,
		)
	lists=list()
	table = soup_classroom.table
	if not table:
		return '-1'
	for tr in table:
                    if type(tr)==Tag:
                        index = -4
                        list_occupy=list()
                        if type(tr.td)==Tag:
                                for i,td in enumerate(tr):
                                        if type(td)==Tag:
                                                index += 1
                                                if td.get('style')!=None:
                                                        list_occupy.append(index)
                        message += updatedata(list_occupy,namestring=tr.contents[0].getText(),\
                    roomtype=tr.contents[1].getText(),\
                   capacity=tr.contents[2].getText(),
                   number=weeknumber
                    )
        return message


def run_update_classroom():
	error = ''
	number = getWeekNumber()
	if number <= 0:
		return '-1'
	else:
		data={}
		data['zhouci'] = str(number)
		data['jxl']='99'
		data['zhouji']='99'
		values=urllib.urlencode(data)
		req=urllib2.Request(urlkb,values)
		response=urllib2.urlopen(req)
		
		string=response.read().decode('gbk')
		
		response.close()
		
		error += handle_classroom(string,number)
		
		number += 1
		#number = 12
		data={}
		data['zhouci'] = str(number)
		data['jxl']='99'
		data['zhouji']='99'
		values=urllib.urlencode(data)
		req=urllib2.Request(urlkb,values)
		response=urllib2.urlopen(req)
		
		string=response.read().decode('gbk')
		
		response.close()
		error += str(number) +':'+ handle_classroom(string,number)
	return error
