#coding=utf-8 
from django.db import models
from django.contrib import admin
from Server import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin   
##class ProfileBase(type):   
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
class sysbug(models.Model):
	content=models.TextField(null=False)
	user=models.ForeignKey(User,to_field='username',null=False)
	rate=models.IntegerField(default=1)
	state=models.IntegerField(choices=((-1,u'已解决'),(0,'正在处理'),(1,u'未解决')))
	time=models.DateTimeField(auto_now=True)

class sysnews(models.Model):
	content=models.TextField(null=False)
	time=models.DateTimeField(auto_now=True)


