# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
import sys

def home(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('index.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/user_panel/')
	else:
		return HttpResponseRedirect('/invalid/')
		
def user_panel(request):
    return render_to_response('user_panel.html')

def invalid_login(request):
    return render_to_response('invalid_login.html')