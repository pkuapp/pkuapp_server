# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
import urllib
import urllib2

from Server.models import Profile
from BeautifulSoup import BeautifulSoup
import re
from xml.sax import make_parser
from xml.sax import parseString
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import unescape
import cStringIO

from django.utils import simplejson
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

hostLibrary = "http://162.105.138.200"
patternQuickSearch = re.compile(u"""form name="searchform" method="post" action="(.+)" onsubmit""")
patternListResult = re.compile(u"(\<li\>[^\.]+Dynamic content lookup(.|\n)+\</li\>)(.|\n)+navigation")
ptReplace = re.compile(u"\<script(.|\n)+?\</script\>")

urlLibrary = "http://162.105.138.200/uhtbin/cgisirsi/0/0/0/49"

def quickSearch(request):
	listBook = list()
	if request.method =='GET':
		page = request.GET.get('page','1')
		query = request.GET.get('q','')
		
		request = urllib2.Request(urlLibrary)
		response = urllib2.urlopen(request)
		string = response.read()
		match = patternQuickSearch.search(string)
		stringQS =  match.group(1)
		
		data = {}
		data['searchdata1'] = query.encode('utf8')
		data['search_type'] = 'search'
		data['library'] = 'ALL'

		urlQS = hostLibrary + stringQS

		values = urllib.urlencode(data)
		request = urllib2.Request(urlQS,values)
		response = urllib2.urlopen(request)
		string =  response.read()
		##filehandler = open('C:/Users/wuhaotian/Desktop/test.htm')
		##string = filehandler.read()
		##filehandler.close()

		matchList = patternListResult.search(string)
		string = matchList.group(1)
		string = ptReplace.sub('',string)
		#string = BeautifulSoup(string).prettify()
		#string = unescape(string,{'&nbsp;':''})


		
		string = """<?xml version="1.0"?>
		<!DOCTYPE note [
		  <!ELEMENT note (ul,li,a,div,script)>
		  <!ELEMENT ul      (#PCDATA)>
		  <!ELEMENT li    (#PCDATA)>
		  <!ELEMENT a (#PCDATA)>
		  <!ELEMENT div    (#PCDATA)>
		  <!ELEMENT dd    (#PCDATA)>
		  <!ELEMENT span    (#PCDATA)>
		  <!ELEMENT input    (#PCDATA)>
		  <!ELEMENT dt    (#PCDATA)>
		  <!ENTITY squot "squot">
		  <!ENTITY quot "quot">
		  <!ENTITY nbsp "nbsp">
		]>""" + string
		stream = cStringIO.StringIO(string)
		parser = make_parser()
		handler = ResultHandler(listBook)
		parser.setContentHandler(handler)
		parser.parse(stream)
		
	return	HttpResponse(simplejson.dumps(listBook),mimetype='application/json')
		
class ResultHandler(ContentHandler):
        def __init__(self,listBook):
                self.isNewItem, self.isTitle,self.isAuthor,self.isTime,self.isHolding = 0,0,0,0,0
                self.listbook = listBook
                
        def startElement(self, name, attrs):
                if name == 'li' and attrs.get('class',None) == 'hit_list_item_info':
                        self.isNewItem = True
                elif name == 'a':
                        self.title = attrs.get('title',None).strip('View Details for  ')
                elif name == 'dd':
                        attr = attrs.get('class',None)
                        if attr == 'author':
                                self.isAuthor = True
                                self.author = ''
                        elif attr is None:
                                self.isTime = True
                                self.time = ''
                        elif attr =='holdings_statement':
                                self.isHolding = True
                                self.holdings = ''
                                
        def endElement(self,name):
                if name == 'li' and self.isNewItem:
                        self.isNewItem = False
                        context = {'tit':self.title,
                                   'aut':self.author,
                                   't':self.time,
                                   'h':self.holdings
                                   }
                        self.listbook.append(context)
                if name == 'dd':
                        self.isAuthor = False
                        self.isTime = False
                        self.isHolding = False
        def characters(self, content):
                content = content.strip('\n')
                if self.isAuthor:
                        self.author = self.author + content
                elif self.isTime:
                    self.time = self.time + content
                elif self.isHolding:
                        self.holdings = self.holdings + content
                


     
