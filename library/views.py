# -*- coding:UTF-8 -*-
if __name__ == "__main__":
    print "main"
else:
    from django.shortcuts import *
    from django.template import RequestContext
    from django.http import HttpResponse
    from django.utils import simplejson
    from django.contrib import auth
    from django import forms
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    from Server.models import Profile
    from django.contrib.auth import login as auth_login
import urllib
import urllib2

from BeautifulSoup import BeautifulSoup
import re
from xml.sax import make_parser
from xml.sax import parseString
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import unescape


def quickSearch(request):
    import library_parser
    page = request.POST.get('page','1')
    query = request.POST.get('q','')
    dom = library_parser.quickSearch({'page':page,'q':query})
    result = library_parser.parseDOM(dom)
    

    return  HttpResponse(simplejson.dumps(result),mimetype='application/json')
        
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
                


     
