import cgi
import urllib

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

@login_required
def player(request):
    return render_to_response('ytplayer.html', context_instance=RequestContext(request))

@login_required
def youtube_vids(request):
    facebook = getattr(request, 'facebook', None)
    if facebook and facebook.uid:
        home_feed = facebook.graph.get_connections('me', 'home', type='video', limit=50)
        vids = (post for post in home_feed['data'] if post['type'] == 'video' and 'youtube.com' in post['link'])
        return HttpResponse(simplejson.dumps(list(vids)))
    else:
        return HttpResponseServerError('not facebook authenticated')

def youtube_vids_stub(request):
    vids = [
        {
            'link': 'http://www.youtube.com/watch?v=V3GmNMbuMbc',
            'from': {'name': 'Christian Bale'},
            'created_time': '00:00 1969'
        },
        {
            'link': 'http://www.youtube.com/watch?v=pX5gRaxcviE',
            'from': {'name': 'Jimi Hendrix'},
            'created_time': '00:00 2010'
        }
    ]
    return HttpResponse(simplejson.dumps(vids))