from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from userprofile.forms import UserCreateForm, UserUpdateForm
from userprofile.models import UserProfile
import random, math, datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import math
from django.conf import settings

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

@login_required(login_url='/')
def user_panel(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    return render_to_response('user_panel.html',{'user_profile':user_profile,'MEDIA_URL':settings.MEDIA_URL})


def invalid_login(request):
    return render_to_response('invalid_login.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreateForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('register.html',args)

@login_required(login_url='/')
def account(request):
    user = User.objects.get(username=request.user.username)
    u = UserProfile.objects.get(user=user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            u.latitude = form.cleaned_data['latitude']
            u.longitude = form.cleaned_data['longitude']
            user.save()
            u.save()
            return HttpResponseRedirect('/account')
        else:
            return HttpResponseRedirect('/account')
    latitude = u.latitude
    longitude = u.longitude
    args = {}
    args.update(csrf(request))
    args['form'] = UserUpdateForm(initial={'latitude':latitude,
                      'longitude':longitude,
                      'first_name':user.first_name,
                      'last_name':user.last_name,
                      'email':user.email})
    args['latitude'] = latitude
    args['longitude'] = longitude
    return render_to_response('account.html', args)
       
@login_required(login_url='/')
def generate(request):
    return HttpResponseRedirect('/maps/')

@login_required(login_url='/')
def maps(request):
    args = {}
    args.update(csrf(request))
    user = User.objects.get(username=request.user.username)
    u = UserProfile.objects.get(user=user)
    latitude = u.latitude
    longitude = u.longitude
    args['latitude'] = u.latitude
    args['longitude'] = u.longitude
    return render_to_response('maps.html', args, context_instance=RequestContext(request))
