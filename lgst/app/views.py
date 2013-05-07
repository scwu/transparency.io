# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import SafeString

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

def organization(request, entityid):
    #top recipients
    if request.method=='GET':
        apikey = '639590fa6001413492a034112c3a6494'
        general = 'http://transparencydata.com/api/1.0/entities/%s.json?apikey=%s' % (entityid, apikey)
        response_g = urllib2.urlopen(url)
        general_total = response.read()
        url = 'http://transparencydata.com/api/1.0/aggregates/org/%s/recipients.json?apikey=%s' % (entityid, apikey)
        response = urllib2.urlopen(url)
        recipients = response.read()
        #party breakdown
        url_party = 'http://transparencydata.com/api/1.0/aggregates/org/%s/recipients/party_breakdown.json?apikey=%s' % (entityid, apikey)
        response_party = urllib2.urlopen(url_party)
        breakdown = response_party.read()
        url_state = 'http://transparencydata.com/api/1.0/aggregates/org/%s/recipients/level_breakdown.json?apikey=%s' % (entityid, apikey)
        response_state = urllib2.urlopen(url_state)
        state_breakdown = response_state.read()
        print state_breakdown
        return render_to_response('organization.html', {'recipients' : SafeString(recipients), 'state_fed' : SafeString(state_breakdown), 'party_breakdown' : SafeString(breakdown)}) 