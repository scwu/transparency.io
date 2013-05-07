# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from app.models import *
import settings, urls
import csv
import urllib
import urllib2

def index(request):
    return render_to_response('index.html')

def get_results(request):
    if request.is_ajax():
        text = request.POST['result'].strip()
        url = 'http://transparencydata.com/api/1.0/entities.json?'
        values = {
            'apikey' : '639590fa6001413492a034112c3a6494',
            'search' : text,
        }
        data = urllib.urlencode(values)
        req = url + data
        response = urllib2.urlopen(req)
        json = response.read()
        return HttpResponse(json)
