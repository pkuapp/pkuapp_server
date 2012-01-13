#coding=utf-8 
from django.db import models
from django.contrib import admin
from Server import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin   
		

	
	
class sms(models.Model):
	content=models.TextField(null=False)
	sendfrom=models.ForeignKey(User,related_name='sentsms',null=False)
	touser=models.ManyToManyField(User,related_name='inbox')
	sendername=models.CharField(max_length=255)
	timestamp=models.DateTimeField(auto_now=True)
	
class sys(models.Model):
	content=models.TextField(null=False)
	sendername=models.CharField(max_length=255)
	timestamp=models.DateTimeField(auto_now=True)
	
class reply(models.Model):
	tocomment=models.ForeignKey('Server.models.comment')
	toreply=models.TextField(null=True)
	touser=models.ForeignKey(User)
	sendfrom=models.ForeignKey(User,related_name='replys')
	sendername=models.CharField(max_length=255)
	timestamp=models.DateTimeField(auto_now=True)
	
class notice(models.Model):
	touser=models.ForeignKey(User)
	ob=models.IntegerField(null=False)
	state=models.BooleanField(default=False)
	sendername=models.CharField(max_length=255)
	ntype=models.IntegerField(choices=((0,u'reply'),(1,u'sys'),(2,u'sms')))
	
	def getnotice(self):
		if self.ntype==0:
			return reply.objects.get(id=notice)
			
		elif self.ntype==1:
			return sys.objects.get(id=notice)
			
		elif self.ntype==2:
			return sms.objects.get(id=notice)
	

		
