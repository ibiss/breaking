from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from userprofile.forms import UserCreateForm
from userprofile.models import Task, Mission, UserProfile, Item
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
    equipment = user_profile.equipment.all()
    base_objects = user_profile.base_objects.all()
    return render_to_response('user_panel.html',{'equimpent':equipment, 'base_object':base_objects,'user_profile':user_profile,'MEDIA_URL':settings.MEDIA_URL})
    #return render_to_response('user_panel.html',{'user_profile':user_profile,'MEDIA_URL':settings.MEDIA_URL})


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
    return render_to_response('register.html', args,context_instance=RequestContext(request))

@login_required(login_url='/')
def account(request):
    user = User.objects.get(username=request.user.username)
    u = UserProfile.objects.get(user=user)
    latitude = u.latitude
    longitude = u.longitude
    return render_to_response('account.html',{'latitude':latitude,'longitude':longitude})
       
@login_required(login_url='/')
def generate(request):#, rfrom, rto):
    usr = User.objects.get(username=request.user.username)
    u = UserProfile.objects.get(user=usr)
    latitude = u.latitude
    longitude = u.longitude
    rfrom = 100
    rto = 1000
    tasks = Task.objects.all()
    while(1):
        radius = random.uniform(rfrom*0.00001, rfrom*0.00001+rto*0.00001)
        angle = random.randint(0,360)
        radians = math.radians(angle)
        t_latitude = math.sin(radians)*radius
        t_longitude = math.cos(radians)*radius
        t_latitude = t_latitude + float(latitude) 
        t_longitude = t_longitude + float(longitude)
        close = math.fabs(t_longitude - float(longitude)) + math.fabs(t_latitude - float(latitude))
        b_near = True
        if(close > 0.0028):
            for t in tasks:
                near = math.fabs(t_longitude - float(t.longitude)) + math.fabs(t_latitude - float(t.latitude))
                if(near < 0.0028):
                    b_near = False
            if(b_near):
                break
    missions = Mission.objects.all()
    m = missions[random.randint(1,len(missions)) - 1]
    task = Task(user_profile=u, mission=m, latitude=t_latitude,longitude=t_longitude,timestamp=datetime.datetime.now())
    task.save()
    return HttpResponseRedirect('/maps/')

@login_required(login_url='/')
def maps(request):
    #try:
        user = User.objects.get(username=request.user.username)
        u = UserProfile.objects.get(user=user)
        latitude = u.latitude
        longitude = u.longitude
     #   try:
        tasks = Task.objects.filter(user_profile_id=u.user_id)
            #t_latitude = t.latitude
            #t_longitude = t.longitude
        return render_to_response('maps.html',{'latitude':latitude,'longitude':longitude,'tasks':tasks})
      #  except:
       #     return render_to_response('maps.html',{'latitude':latitude,'longitude':longitude})
   # except:
    #    return HttpResponseRedirect('/')
