# -*- coding:UTF-8 -*-
import urllib
import urllib2
import cookielib

from BeautifulSoup import BeautifulSoup
import re

hostLibrary = "http://162.105.138.200"
patternQuickSearch = re.compile(u"""<form name="searchform" method="post" action="(.+)/123">""")
patternListResult = re.compile(u"(\<li\>[^\.]+Dynamic content lookup(.|\n)+\</li\>)(.|\n)+navigation")
ptReplace = re.compile(u"\<script(.|\n)+?\</script\>")

urlLibrary = "http://162.105.138.200/uhtbin/cgisirsi/0/0/0/49"

def quickSearch(request):
    listBook = list()
    page = request.get('page','1')
    query = request.get('q','')
    
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'),
    ] 
    
    
    request = urllib2.Request(urlLibrary)
    response = opener.open(request)
    string = response.read()
    match = patternQuickSearch.search(string)
    if match is None:
        return ''
    stringQS =  match.group(1)

    data = {}
    data['searchdata1'] = query.encode('utf8')
    #data['search_type'] = 'searchengine'
    data['library'] = 'ALL'
    data['sort_by'] = 'relevance'
    data['user_id'] = 'WEBSERVER'
    urlQS = hostLibrary + stringQS + '/123'
    values = urllib.urlencode(data)
    response = opener.open(urlQS,values)
    
    offset = 20 * (int(page)-1) + 1
    opener.addheaders += [ ('Referer', urlQS)]
    
    data = {}
    
    data['form_type'] = 'JUMP^' + str(offset)
    #data['form_type'] = u'JUMP^41' 
    urlPage = hostLibrary + stringQS + '/9'
    
    values = urllib.urlencode(data)
    response = opener.open(urlPage,values)
    
    string =  response.read()
    ##filehandler = open('C:/Users/wuhaotian/Desktop/test.htm')
    ##string = filehandler.read()
    ##filehandler.close()

    matchList = patternListResult.search(string)
    if matchList is None:
        return ''
    string = matchList.group(1)
    string = ptReplace.sub('',string)
    return string

def parseDOM(aunicode):
    keywords = {}
    keywords['class'] = "hit_list_item_info"
    soup_li = BeautifulSoup(aunicode)
    ul_items = soup_li.findAll('li',**keywords)
    result = list()
    from BeautifulSoup import Tag as BTag
    
    for i,li in enumerate(ul_items):
        dl = li.contents[1]
        context = {}

        for atag in dl:
            if not isinstance(atag,BTag):
                continue
            class_info = atag.get('class','')
            if atag.name == 'dd' and class_info == "title":
                context['title'] = atag.contents[1].contents[2].strip()
            elif class_info  == 'author':
                context['author'] = atag.contents[2].strip()
            elif class_info  == 'call_number':
                context['call'] = atag.contents[2].strip()
            elif class_info == 'holdings_statement':
                context['holding'] = atag.contents[2].strip()

        result.append(context)
    
    return result

if __name__== "__main__":
    aunicode = quickSearch({'page':'3',
        'q':u"Rails"})
    print parseDOM(aunicode)
        

     
