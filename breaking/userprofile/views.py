from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from userprofile.forms import UserCreateForm, UserUpdateForm, MessageForm, QueueForm
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

@login_required(login_url='/')
def joinQueue(request):
    usr=User.objects.get(username=request.user.username)
    usrProfile=UserProfile.objects.get(user=usr)
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            result = Queue.objects.filter(mode=form.cleaned_data['gameMode'])
            result = result[0]
            if result:
                gInstance = GameInstance(
                    player1=result.player,
                    player2=usrProfile,
                    dateTime1=datetime.datetime.now(),
                    dateTime2=datetime.datetime.now(),
                    available=True,
                    mode=result.mode)
                gInstance.save()
                checkpoint = generateCheckpoint(result.player, usrProfile, gInstance)
                checkpoint.save()
                result.delete()
            else:
			    queuePVP = Queue(player=usrProfile, mode=form.cleaned_data['gameMode'])
			    queuePVP.save()
            return HttpResponseRedirect('/challenge/')
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
            print 'if'
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
                    msg = MessageBox.objects.filter(fromUser=User.objects.get(username=request.user.username),toUser=userid)
                except MessageBox.DoesNotExist:
                    print'safsa';
                try:
                    msg2 = MessageBox.objects.filter(fromUser=userid,toUser=User.objects.get(username=request.user.username))
                except MessageBox.DoesNotExist:
                    print'safsa';
		c = Context({'contacts':contacts,'msg':msg,'msg2':msg2,'username':User.objects.get(id=userid).username,'form':form}) 
                return render_to_response('messagebox.html', c,
			context_instance=RequestContext(request))
        else:
            print 'else'
            contacts = User.objects.all
            try:
                msg = MessageBox.objects.filter(fromUser=User.objects.get(username=request.user.username),toUser=userid)
            except MessageBox.DoesNotExist:
                print'safsa';
            try:
                msg2 = MessageBox.objects.filter(fromUser=userid,toUser=User.objects.get(username=request.user.username))
            except MessageBox.DoesNotExist:
                print'safsa';
            form = MessageForm(request.POST)
            d = {}
            d.update(csrf(request))
            t = loader.get_template("messagebox.html")
            c = Context({'contacts':contacts,'msg':msg,'msg2':msg2,'username':User.objects.get(id=userid).username,'form':form})  
	    return render_to_response('messagebox.html', c,
			context_instance=RequestContext(request))

