from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import Task, Mission, UserProfile, Item
import random, math

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
'''
def user_panel(request):
    return render_to_response('user_panel.html')
'''
def invalid_login(request):
    return render_to_response('invalid_login.html')
	
def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
			
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	return render_to_response('register.html', args)

def account(request):
        return render_to_response('account.html')

def user_panel(request):
	#username = request.user.username
	user = UserProfile.objects.get(first_name='test')
	latitude = user.latitude
	longitude = user.longitude
	radius = random.uniform(0.0001,0.0300)
	angle = random.randint(0,360)
	radians = math.radians(angle)
	t_latitude = math.sin(radians)*radius
	t_longitude = math.cos(radians)*radius
	t_latitude = t_latitude + float(latitude)
	t_longitude = t_longitude + float(longitude)
	return render_to_response('user_panel.html',{'t_latitude':t_latitude,'t_longitude':t_longitude})
