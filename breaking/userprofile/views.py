# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from userprofile.forms import UserCreateForm, UserUpdateForm, MessageForm, QueueForm, ChangeQueueTimeForm
from userprofile.models import UserProfile, MessageBox, Queue, GameInstance, Subcategory, Checkpoint
import random, math, datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#import math
from django.conf import settings
from django.template import loader, Context
from django.db.models import Q
import datetime
from funcCoord import generateCheckpoint
from functions import offsetTime, makeGameInstance, challengeRequest

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
    return render_to_response('user_panel.html',{
        'user_profile':user_profile,
        'MEDIA_URL':settings.MEDIA_URL
        })


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
def maps(request):
    args = {}
    args.update(csrf(request))
    user = User.objects.get(username=request.user.username)
    usrProfile = UserProfile.objects.get(user=user)
    gInstances = GameInstance.objects.filter(player1=usrProfile) | GameInstance.objects.filter(player2=usrProfile)
    checkpoints = {}

    counter = 0
    for g in gInstances:
        cs = Checkpoint.objects.filter(game=g)
        for c in cs:
            if(g.player1.user.username == user.username):
                checkpoints[counter] = [c.latitudeP1, c.longitudeP1]
                counter = counter + 1;
            else:
                checkpoints[counter] = [c.latitudeP2, c.longitudeP2]
                counter = counter + 1;

    latitude = usrProfile.latitude
    longitude = usrProfile.longitude
    args['latitude'] = usrProfile.latitude
    args['longitude'] = usrProfile.longitude
    args['checkpoints'] = checkpoints
    args['gamesInProgress'] = gInstances
    args['now_date'] = datetime.datetime.now();
    return render_to_response('maps.html', args, context_instance=RequestContext(request))

@login_required(login_url='/')
def joinQueue(request):
    usr=User.objects.get(username=request.user.username)
    usrProfile=UserProfile.objects.get(user=usr)
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            timeStart = int(form.cleaned_data['timeStart'])
            timeEnd = int(form.cleaned_data['timeEnd'])
            result = Queue.objects.filter(mode=form.cleaned_data['gameMode'])
            challengeRequest(result,timeStart,timeEnd,usrProfile,form)
            return HttpResponseRedirect('/challenge/')
        form = ChangeQueueTimeForm(request.POST)
        if form.is_valid():
            timeStart = int(form.cleaned_data['timeStart'])
            timeEnd = int(form.cleaned_data['timeEnd'])
            result = Queue.objects.filter(mode=form.cleaned_data['gameMode'],player=usrProfile).update(timeStart=timeStart, timeEnd=timeEnd)
    else:
        form = QueueForm()
    waitingGames = Queue.objects.filter(player=usrProfile)
    gamesInProgress = GameInstance.objects.filter(player1=usrProfile) | GameInstance.objects.filter(player2=usrProfile)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['waitingGames'] = waitingGames
    args['gamesInProgress'] = gamesInProgress
    return render_to_response('challenge.html',args)

@login_required(login_url='/')
def messagebox_view(request):
    contacts = User.objects.all
    t = loader.get_template("messagebox.html")
    c = Context({'contacts':contacts})
    return HttpResponse(t.render(c))

@login_required(login_url='/')
def message_view(request,userid):
        if request.method == 'POST':
            form = MessageForm(request.POST)
	    if form.is_valid():
		cd = form.cleaned_data
		contacts = MessageBox(description=cd['description'],
                                    fromUser=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
                                    ,toUser=UserProfile.objects.get(user=User.objects.get(id=userid)))#timestamp=datetime.now()
		contacts.save()
		contacts = User.objects.all
		form = MessageForm(request.POST)
		try:
                    messages = MessageBox.objects.filter(fromUser=User.objects.get(username=request.user.username),toUser=userid)
                except MessageBox.DoesNotExist:
                    raise Exception('MessageBox does not exist')
                try:
                    messages2 = MessageBox.objects.filter(fromUser=userid,toUser=User.objects.get(username=request.user.username))
                except MessageBox.DoesNotExist:
                    raise Exception('MessageBox does not exist')
		c = Context({'contacts':contacts,'messages':messages,'messages2':messages2,'username':User.objects.get(id=userid).username,'form':form}) 
                return render_to_response('messagebox.html', c,
			context_instance=RequestContext(request))
        else:
            contacts = User.objects.all
            try:
                messages = MessageBox.objects.filter(fromUser=User.objects.get(username=request.user.username),toUser=userid)
            except MessageBox.DoesNotExist:
                raise Exception('MessageBox does not exist')
            try:
                messages2 = MessageBox.objects.filter(fromUser=userid,toUser=User.objects.get(username=request.user.username))
            except MessageBox.DoesNotExist:
                raise Exception('MessageBox does not exist')
            form = MessageForm(request.POST)
            d = {}
            d.update(csrf(request))
            t = loader.get_template("messagebox.html")
            c = Context({'contacts':contacts,
                'messages':     messages,
                'messages2':    messages2,
                'userTarget':   User.objects.get(id=userid).username,
                'form':         form
                })  
	    return render_to_response('messagebox.html', c,context_instance=RequestContext(request))
