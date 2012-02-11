#coding=utf-8 

from django.db import models
from django.contrib import admin
from Server import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin   
import re
from django.forms.models import model_to_dict

psingle=re.compile(u'单')
pdouble=re.compile(u'双')
pmath=re.compile(u'[0-9]+')


list_building_old =[u"一教",u"二教",u"三教",u"四教",u"文史楼",\
		u"电教",u"哲学",u"物理",u"地学",u"技物",\
		u"外文",u"体教",u"数学",u"化学",u"电子",\
		u"理教",u"电教听力",u"国关",u"政管",u"光华",\
		u"理科2#"]

list_building=[u"一教",u"二教",u"三教",u"四教",u"文史[楼]*",\
		u"电教",u"哲学",u"物理",u"地学",u"技物",\
		u"外文",u"体教",u"数学",u"化学",u"电子",\
		u"理教",u"电教听力",u"国关",u"政管",u"光华",\
		u"理科2#"]
		
list_day = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']
list_re=[re.compile(x +' *'+ u'([a-zA-Z0-9-]+)') for x in list_building]
re_inter=re.compile(u'[a-zA-Z0-9-]+')
re_time=re.compile(u'[每|单|双]周周(.?)([0-9]+)~([0-9]+)')

##class ProfileBase(type):   
##    
##    def __new__(cls, name, bases, attrs):   
##         module = attrs.pop('__module__')   
##         parents = [b for b in bases if isinstance(b, ProfileBase)]   
##         if parents:   
##            fields = []   
##            for obj_name, obj in attrs.items():   
##                if isinstance(obj, models.Field): 
##                	fields.append(obj_name)   
##                User.add_to_class(obj_name, obj)   
##            UserAdmin.fieldsets = list(UserAdmin.fieldsets)   
##            UserAdmin.fieldsets.append((name, {'fields': fields}))   
##         return super(ProfileBase, cls).__new__(cls, name, bases, attrs)   
##           
##class Profile(object):   
##     __metaclass__ = ProfileBase   
  

class place(models.Model):
	name = models.CharField(u'教室名',max_length=50,blank=False)
	location = models.CharField(null=False,max_length=5)
	interid = models.CharField(null=False,max_length=20)
	keyid = models.CharField(primary_key=True,max_length=20,null=False)
	roomtype = models.CharField(max_length=5,null=True)
	rcapacity = models.CharField(max_length=10)
	feedback = models.IntegerField(default=-1)
	feedbacktime = models.DateTimeField(auto_now=True,null=True)
	
	@staticmethod
	def dictFromPlaceString(pstring):
		"elective的两份课程地点及课程时间会写在一起，dictFromPlaceString只返回后者"
		if pstring == '':
			return None
		
		for i in range(21):
			m1 = re.search(list_re[i],pstring)
			if m1:
				m2 = re.search(list_re[i],pstring[m1.end():])
				if m2:
					return {'location':i+1,
						'placename':m2.group(0),
						'interid':m2.group(1)
					}
				else:
					return {'location':i+1,
						'placename':m1.group(0),
						'interid':m1.group(1)
					}
		return None
	
class School(models.Model):
	code = models.CharField('SchoolCode',max_length=10,blank=False)
	name = models.CharField('name',max_length=75,blank=False)
	ename = models.CharField('ename',max_length=75,blank=False)
	
	
class placet(models.Model):
	day1=models.IntegerField(null=False) 	
	day2=models.IntegerField(null=False) 	
	day3=models.IntegerField(null=False) 	
	day4=models.IntegerField(null=False) 	
	day5=models.IntegerField(null=False) 	
	day6=models.IntegerField(null=False) 	
	day7=models.IntegerField(null=False) 	
	weeknumber=models.IntegerField(null=False)
	place=models.ForeignKey(place)
	@staticmethod
	def dayCodeFromWeekStateList(i,list_day):
		"list_day 包含0 ～ （7*12-1）的节序号，如周一为 0 ～11 节，周二为12～23节"
		daycode = 0
		for daynumber in list_day:
			daynumber = daynumber -12*(i-1)
			if daynumber >= 0 and daynumber < 12:
				daycode += 2**daynumber
		return daycode

class teacher(models.Model):
	name = models.CharField(max_length=50)
	
class course(models.Model):
	termnumber = models.IntegerField()
	courseid = models.CharField(max_length=50)
	keyid = models.CharField(max_length=50)
	name = models.CharField(max_length=255)
	classnum = models.CharField(max_length=10)
	rawplace = models.CharField(max_length=50,null=True)
	time_test = models.CharField(max_length=75,null=True)
	credit = models.CharField(max_length=5)
	time = models.CharField(max_length=50)
	day1 = models.IntegerField(null=False) 	
	day2 = models.IntegerField(null=False) 	
	day3 = models.IntegerField(null=False) 	
	day4 = models.IntegerField(null=False) 	
	day5 = models.IntegerField(null=False) 	
	day6 = models.IntegerField(null=False) 	
	day7 = models.IntegerField(null=False)
	place = models.ForeignKey(place,null=True)
	teachername = models.CharField(max_length=20)
	teacherid = models.ForeignKey(teacher,null=True)
	manager = models.ManyToManyField(User)
	user = models.ManyToManyField(User)
	course_category = models.IntegerField(choices=((0,u'校本部'),(1,u'研究生')))
	
	Coursetype = models.CharField(max_length=10,null=True)
	SchoolCode = models.CharField(max_length=10,null=True)
	txType = models.CharField(max_length=10,null=True)

	cname = models.CharField(max_length=255,null=True)
	ename = models.CharField(max_length=255,null=True)
	class Meta:
		db_table = 'server_course'
		
	def cname(self):
		'this function is NOT completed yet.'
		p = re.compile(u"""([a-zA-Z]*[()A-Za-z0-9]*$)""")
		
	def get_time_display(self):
		"Deprecated"
		context={}
		for x in range(1,8):
			dayx=getattr(self,'day'+ str(x))
			
			if dayx!=0:
				daystring=bin(dayx)
				codestring=daystring[-min(len(daystring),14)+2:]
				end=len(codestring)-codestring.find('1')
				temp=list(codestring)
				temp.reverse()
				null=''
				temp=null.join(temp)
				beg=temp.find('1')+1
				
				daycode=beg+end*(2**4)
				if len(daystring)>14:
					daycode+=2**(len(daystring)-3)
				context['day'+str(x)]=daycode
			else:
				context['day'+str(x)]=0
		return context
	@staticmethod
	def daydataFromDayString(daystring):
		"course的节标注 格式如 3-4 3～4"
		daydata = 0
		if daystring!='':
				match = re.findall(pmath,daystring)
				if match:
					daydata = int(match[0]) + int(match[1])*(2**4)
					if re.search(psingle,daystring):
						daydata+=2**8
					elif re.search(pdouble,daystring):
						daydata+=2**9
		return daydata

class Profile(models.Model):
	realname = models.CharField(max_length=50)
	school = models.CharField(max_length=50,blank=False)
	major = models.CharField(max_length=50,blank=False)
	grade = models.CharField(max_length=20,blank=False)
	mphone = models.CharField(max_length=20,blank=True)
	phone = models.CharField(max_length=20,blank=True)
	
	user_type = models.IntegerField(choices=((0,u'校本部'),(1,u'研究生')))
	teach_courses = models.ManyToManyField(course)
        user=models.OneToOneField(User)

class Assignment(models.Model):
	content = models.CharField(max_length = 755,blank = True)
	deadline = models.DateTimeField(null = True)
	tocourse = models.ForeignKey(course)	

class comment(models.Model):
	timestamp=models.DateTimeField(auto_now=True)
	content=models.TextField(null=False)
	course=models.ForeignKey('course',null=True)
	place=models.ForeignKey('place',null=True)
	user=models.ForeignKey(User,null=True)
	sendername=models.CharField(max_length=255)
	class Meta:
		ordering = ['-timestamp']	

	
class sms(models.Model):
	title=models.CharField(max_length=255,null=True)
	content=models.TextField(null=False)
	sendfrom=models.ForeignKey(User,related_name='sentsms',null=False)
	touser=models.ManyToManyField(User,related_name='inbox')
	sendername=models.CharField(max_length=255)
	timestamp=models.DateTimeField(auto_now=True)
	state=models.BooleanField(default=False)
	class Meta:
		ordering = ['-timestamp']
		
class sys_notice(models.Model):
	title=models.CharField(max_length=255,null=True)
	content=models.TextField(null=False)
	sendername=models.CharField(max_length=255)
	timestamp=models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-timestamp']
		
class reply(models.Model):
	tocomment=models.ForeignKey(comment)
	toreply=models.TextField(null=True)
	touser=models.ForeignKey(User)
	sendfrom=models.ForeignKey(User,related_name='replys')
	sendername=models.CharField(max_length=255)
	content=models.TextField(null=False)
	timestamp=models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-timestamp']
	
class notice(models.Model):
	touser=models.ForeignKey(User)
	obj_id=models.IntegerField(null=False)
	state=models.BooleanField(default=False)
	sendername=models.CharField(max_length=255)
	ntype=models.IntegerField(choices=((0,u'reply'),(1,u'sys'),(2,u'sms')))
	
	def getnotice(self):
		if self.ntype==0:
			return comment.objects.get(id=self.obj_id).content
			
		elif self.ntype==1:
			return model_to_dict(sys_notice.objects.get(id=self.obj_id))
			
		elif self.ntype==2:
			return sms.objects.get(id=self.obj_id).title
