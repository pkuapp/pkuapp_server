# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse

from Server.models import *
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime


def get_all(request):
    keyword = request.GET.get('keyword', None)
    category_id = request.GET.get('category', None)
    after = request.GET.get('after', None)
    before = request.GET.get('before', None)
    start = request.GET.get('start', None)
    batch = request.GET.get('batch', None)
    
    activity_objs = Activity.objects.all()
    if keyword:
        activity_objs = activity_objs.filter(title__contains=keyword)
    if category_id:
        activity_objs = activity_objs.filter(category=category_id)
    if after:
        activity_objs = activity_objs.filter(time__gte=datetime.fromtimestamp(float(after)))
    else:
        activity_objs = activity_objs.filter(time__gte=datetime.now())
    if before:
        activity_objs = activity_objs.filter(time__lte=datetime.fromtimestamp(float(before)))
    if not start:
        start = 0
    if not batch:
        batch = 10
    activity_objs = activity_objs[int(start):int(batch)]
    
    activity_values = activity_objs.values()
    for i in range(len(activity_values)):
        activity_values[i]['time'] = activity_values[i]['time'].isoformat(' ')
        activity_values[i]['category_name'] = ActivityCategory.objects.get(pk=activity_values[i]['category_id']).name
        activity_values[i]['follow_count'] = int(activity_objs[i].follow_count())
    
    return HttpResponse(simplejson.dumps(list(activity_values)), mimetype='application/json')


def get_category(request):
    category_objs = ActivityCategory.objects.all()
    category_values = list(category_objs.values())

    for i in range(len(category_values)):
        category_values[i]['count'] = category_objs[i].count()

    return HttpResponse(simplejson.dumps(category_values), mimetype='application/json')


def get_item(request):
    activity_id = request.GET.get('id', None)
    
    if activity_id:
        try:
            activity_queryset = Activity.objects.filter(pk=int(activity_id))
            activity_obj = activity_queryset[0]
            activity = activity_queryset.values()[0]
            activity['time'] = activity['time'].isoformat(' ')
            activity['category_name'] = ActivityCategory.objects.get(pk=activity['category_id']).name
            activity['follow_count'] = int(activity_obj.follow_count())
            return HttpResponse(simplejson.dumps(activity), mimetype='application/json')
        except:
            return HttpResponse('-4')
            
    return HttpResponse('-3')


# TODO
def follow(request):
    pass


# TODO
def get_following(request):
    pass
