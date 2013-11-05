# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context

def home(request):
	return render_to_response('index.html');
