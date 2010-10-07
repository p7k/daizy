import cgi
import urllib

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

import facebook_sdk as fb

# Find a JSON parser
try:
    import json
    _write_json = lambda s: json.dumps(s)
except ImportError:
    try:
        import simplejson
        _write_json = lambda s: simplejson.dumps(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _write_json = lambda s: simplejson.dumps(s)

def login(request):
    error = None
    vid_list = ''

    fb_cookie = fb.get_user_from_cookie(
        request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    if fb_cookie:
        access_token = fb_cookie['access_token']
        user = auth.authenticate(access_token=access_token)

        # haxor into here
        # graph = fb.GraphAPI(access_token)
        # import ipdb; ipdb.set_trace()
        # home_feed = graph.get_connections('me', 'home', type='video', limit=100)
        # vids = (post for post in home_feed['data'] if post['type'] == 'video')
        # html_unit = "<div><p>From: %(from)s</p><p>Link: %(link)s</p><p>Date: %(created_time)s</p></div>"
        # vid_list = "<br/>".join(
        #     [html_unit % vid for vid in vids]
        # )

        if user:
            if user.is_active:
                auth.login(request, user)
                # return HttpResponseRedirect('/')
            else:
                error = 'AUTH_DISABLED'
        else:
            error = 'AUTH_FAILED'
    elif 'error_reason' in request.GET:
        error = 'AUTH_DENIED'
    else:
        auth.logout(request)

    template_context = {'error': error, 'vids': vid_list}
    return render_to_response('index.html', template_context, context_instance=RequestContext(request))

@login_required
def youtube_vids(request):
    fb_cookie = fb.get_user_from_cookie(
        request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    if fb_cookie:
        access_token = fb_cookie['access_token']
        user = auth.authenticate(access_token=access_token)

        graph = fb.GraphAPI(access_token)
        home_feed = graph.get_connections('me', 'home', type='video', limit=50)
        vids = (post for post in home_feed['data'] if post['type'] == 'video' and 'youtube.com' in post['link'])
        return HttpResponse(_write_json(list(vids)))
    return HttpResponseServerError()


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
    return HttpResponse(_write_json(vids))