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
    try:
        user = User.objects.get(username=request.user.username)
        u = UserProfile.objects.get(user=user)
        latitude = u.latitude
        longitude = u.longitude
        try:
            t = Task.objects.get(user_id=u.user_id)
            t_latitude = t.latitude
            t_longitude = t.longitude
            return render_to_response('user_panel.html',{'latitude':latitude,'longitude':longitude,'t_latitude':t_latitude,'t_longitude':t_longitude})
        except:
            return render_to_response('user_panel.html',{'latitude':latitude,'longitude':longitude})
    except:
        return HttpResponseRedirect('/')    
    '''if t:
        t_latitude = t.latitude
        t_longitude = t.longitude
        return render_to_response('user_panel.html',{'latitude':latitude,'longitude':longitude,'t_latitude':t_latitude,'t_longitude':t_longitude})
    else:
        return render_to_response('user_panel.html',{'latitude':latitude,'longitude':longitude})'''

def invalid_login(request):
    return render_to_response('invalid_login.html')
    
def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
            
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreateForm()
    return render_to_response('register.html', args)

def account(request):
    user = User.objects.get(username=request.user.username)
    u = UserProfile.objects.get(user=user)
    latitude = u.latitude
    longitude = u.longitude
    return render_to_response('account.html',{'latitude':latitude,'longitude':longitude})
       
def generate(request):
    try:
        usr = User.objects.get(username=request.user.username)
        u = UserProfile.objects.get(user=usr)
        t = Task.objects.get(user_id=u.user_id)
    #    t_latitude = t.latitude
    #    t_longitude = t.longitude
        return HttpResponseRedirect('/user_panel/')
    except:
        #usr = User.objects.get(username=request.user.username)
        #u = UserProfile.objects.get(user=usr)
        latitude = u.latitude
        longitude = u.longitude
        radius = random.uniform(0.00001,0.0300)
        angle = random.randint(0,360)
        radians = math.radians(angle)
        t_latitude = math.sin(radians)*radius
        t_longitude = math.cos(radians)*radius
        t_latitude = t_latitude + float(latitude)
        t_longitude = t_longitude + float(longitude)
        missions = Mission.objects.all()
        m = missions[random.randint(1,len(missions))-1]
        task = Task(user=u, mission=m, latitude=t_latitude,longitude=t_longitude,timestamp=datetime.datetime.now())
        task.save()
        return HttpResponseRedirect('/user_panel/')
        #return render_to_response('user_panel.html',{'latitude':latitude,'longitude':longitude,'t_latitude':t_latitude,'t_longitude':t_longitude})
