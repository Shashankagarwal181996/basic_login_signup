# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext

from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *

import datetime
import math

def index(request):
	context_list = {}
	return render(request,'index.html',context_list)


def signin(request):
	if request.POST:
		email = request.POST.get('email')
		password = request.POST.get('password')
		# print email
		user = User.objects.filter(email=email)
		# print user
		if len(user) != 0:
			user = authenticate(username = user[0].username,password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					request.session['userid'] = user.id
					return HttpResponse("Successfully login")
				else:
					return HttpResponseRedirect("/index/")
			else:
				state = "Password is incorrect."
				print state
				context_list = {
					'state': state,
				}
				return render(request,'index.html',context_list)
		else:
			state = "Please signup to login."
			context_list = {
				'state': state,
			}
			return render(request,'index.html',context_list)

def register(request):
	context_list = {}
	return render(request,'signup.html',context_list)

def signup(request):
	if request.POST:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		us = username
		username=email                 #### We are taking username same as email
		if password == confirm_password:
			user = User.objects.create_user(username=username,email=email,password=password)
			user.first_name = first_name
			user.last_name = last_name
			user.username = us
			user.email = email
			request.session['userid'] = user.id
			user.save()
			user.is_active = True
			context_list = {}
			return HttpResponseRedirect("/index/")
		else:
			state = "Passwords do not match."
			print state
			context_list = {
				'state': state,
			}
			return render(request,'signup.html',context_list)
