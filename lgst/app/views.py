# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import SafeString

from app.models import *
import settings, urls
import csv
import urllib
import urllib2
import json
import re

from app.wikipedia import Wikipedia, WikipediaError
from app.wiki2plain import Wiki2Plain

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
        if json == "[]":
            query2 = re.sub(r'[^a-zA-Z0-9 ]', '', text)
            url2 = 'http://transparencydata.com/api/1.0/entities.json?'
            values2 = {
                'apikey' : '639590fa6001413492a034112c3a6494',
                'search' : query2,
            }
            data2 = urllib.urlencode(values2)
            req2 = url2 + data2
            response2 = urllib2.urlopen(req2)
            json = response2.read()
        return HttpResponse(json)

def organization(request, entityid):
    #top recipients
    if request.method=='GET':
        apikey = '639590fa6001413492a034112c3a6494'
        general = 'http://transparencydata.com/api/1.0/entities/%s.json?apikey=%s' % (entityid, apikey)
        response_g = urllib2.urlopen(general)
        general_total = response_g.read()
        done = json.loads(general_total)
        name = done['name']
        try:
            bio = done['metadata']['bio']
            result = re.compile('<p>(.*)</p>', re.DOTALL ).search(bio)
            try:
                bio = result.group(1)
            except:
                pass
            photo = done['metadata']['photo_url']
        except:
            url_encode2 = re.sub(r'[^a-zA-Z0-9 ]', '', name)
            final_str = ' '.join(url_encode2.split())
            url_encode = final_str.replace(" ", "+")
            wiki_search = "http://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=%s&srlimit=1" % (url_encode)
            results = urllib2.urlopen(wiki_search)
            results_dict = json.loads(results.read())
            title = results_dict['query']['search'][0]['title']
            lang = 'en'
            wiki_p = Wikipedia(lang)
            try:
                raw = wiki_p.article(title)
            except:
                raw = None
            if raw:
                wiki2plain = Wiki2Plain(raw)
                content = str(wiki2plain.text)
                result = re.compile('}}(.*)==History==', re.DOTALL).search(content)
                try:
                    bio = result.group(1)
                    result2 = re.compile('<p>(.*)<\/p>', re.DOTALL).search(bio)
                    try:
                        bio = result2.group(1)
                    except:
                        pass
                except:
                    try:
                        bio = content.split("==History==",1)[0]
                        result2 = re.compile('<p>(.*)<\/p>', re.DOTALL).search(bio)
                        try:
                            bio = result2.group(1)
                        except:
                            pass
                    except: 
                        bio = None
            else:
                bio = None
            photo = None
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
        #get pac breakdown
        url_pac = 'http://transparencydata.com/api/1.0/aggregates/org/%s/recipient_pacs.json?apikey=%s' % (entityid, apikey)
        response_pac = urllib2.urlopen(url_pac)
        pac_breakdown = response_pac.read()
        #get top lobbyists
        url_lobbying = 'http://transparencydata.com/api/1.0/aggregates/org/%s/registrants.json?apikey=%s' % (entityid, apikey)
        response_lobbyist = urllib2.urlopen(url_lobbying)
        lobbyist_breakdown = response_lobbyist.read()
        #get top issues
        url_issues = 'http://transparencydata.com/api/1.0/aggregates/org/%s/issues.json?apikey=%s' % (entityid, apikey)
        response_issues = urllib2.urlopen(url_issues)
        issues_breakdown = response_issues.read()
        #top bills
        url_bills = 'http://transparencydata.com/api/1.0/aggregates/org/%s/bills.json?apikey=%s' % (entityid, apikey)
        response_bills = urllib2.urlopen(url_bills)
        bills_breakdown = response_bills.read()
        processor = {
                     'recipients' : SafeString(recipients),
                     'state_fed' : SafeString(state_breakdown),
                     'party_breakdown' : SafeString(breakdown),
                     'lobbyist' : SafeString(lobbyist_breakdown),
                     'pac' : SafeString(pac_breakdown),
                     'bio' : bio.strip(),
                     'name' : name.upper(),
                     'bills' : SafeString(bills_breakdown),
                     'issues_breakdown' : SafeString(issues_breakdown),
                     'photo' : photo
        }
        return render_to_response('organization.html', processor)
