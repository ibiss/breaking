from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from userprofile.forms import UserCreateForm, UserUpdateForm, CommunicatorForm
from userprofile.models import UserProfile, Communicator
import random, math, datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import math
from django.conf import settings
from django.template import loader, Context

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
<<<<<<< HEAD

def join_1v1(request):
	if request.method == 'POST':
		form = JoinPVPForm(request.POST)
		if form.is_valid():
			usr=User.objects.get(username=request.user.username)
			joinPVP = JoinPVP(player=UserProfile.objects.get(user=usr), mode=form.cleaned_data['gameMode'])
			joinPVP.save()
			# wybor zawodnika ###########################################
#				if Join_1v1.objects.all() == null: #create new player, who has to wait for another player
#					joinObject = Join_1v1(player=request.user)
#					joinObject.save()
#					#return czekam na zawodnika
#				else: #get player for queue and create game with new player
#					play1 = Join_1v1.objects.all()
#					play2 = request.user
#					game = Game_1v1(player1=play1, player=play2, available=False)
#					game.save()
#					Join_1v1.objects.all().delete()
				#return zawodnik znaleziony, wybierz date i godzine
			##########################################################
			return HttpResponseRedirect('/challenge/')
	else:
		form = JoinPVPForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render_to_response('challenge.html',args)
=======
@login_required(login_url='/')
def communicator_view(request):
    coms = User.objects.all
    t = loader.get_template("communicator.html")
    c = Context({'coms':coms})
    return HttpResponse(t.render(c))
@login_required(login_url='/')
def communicator_view_id(request,userid):
        if request.method == 'POST':
            print 'if'
            form = CommunicatorForm(request.POST)
	    if form.is_valid():
		cd = form.cleaned_data
		coms = Communicator(description=cd['description'],
                                    user_profile=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
                                    ,user_addressee=UserProfile.objects.get(user=User.objects.get(id=userid)))#timestamp=datetime.now()
		coms.save()
		coms = User.objects.all
		form = CommunicatorForm(request.POST)
		try:
                    msg = Communicator.objects.filter(user_profile=User.objects.get(username=request.user.username),user_addressee=userid)
                except Communicator.DoesNotExist:
                    print'safsa';
                try:
                    msg2 = Communicator.objects.filter(user_profile=userid,user_addressee=User.objects.get(username=request.user.username))
                except Communicator.DoesNotExist:
                    print'safsa';
		c = Context({'coms':coms,'msg':msg,'msg2':msg2,'username':User.objects.get(id=userid).username,'form':form}) 
                return render_to_response('communicator.html', c,
			context_instance=RequestContext(request))
        else:
            print 'else'
            coms = User.objects.all
            try:
                msg = Communicator.objects.filter(user_profile=User.objects.get(username=request.user.username),user_addressee=userid)
            except Communicator.DoesNotExist:
                print'safsa';
            try:
                msg2 = Communicator.objects.filter(user_profile=userid,user_addressee=User.objects.get(username=request.user.username))
            except Communicator.DoesNotExist:
                print'safsa';
            form = CommunicatorForm(request.POST)
            d = {}
            d.update(csrf(request))
            t = loader.get_template("communicator.html")
            c = Context({'coms':coms,'msg':msg,'msg2':msg2,'username':User.objects.get(id=userid).username,'form':form})  
	    return render_to_response('communicator.html', c,
			context_instance=RequestContext(request))

>>>>>>> master
