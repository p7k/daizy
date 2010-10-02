import cgi
import urllib

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

import facebook_sdk as fb

def login(request):
    error = None
    vid_list = ''

    fb_cookie = fb.get_user_from_cookie(
        request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    if fb_cookie:
        access_token = fb_cookie['access_token']
        user = auth.authenticate(access_token=access_token)

        # haxor into here
        graph = fb.GraphAPI(access_token)
        import ipdb; ipdb.set_trace()
        home_feed = graph.get_connections('me', 'home', type='video', limit=100)
        vids = (post for post in home_feed['data'] if post['type'] == 'video')
        html_unit = """<div>
    <label>From: %(from)s</label>
    <object width="480" height="385">
        <param name="movie" value="%(link)s"></param>
        <param name="allowFullScreen" value="true"></param>
        <param name="allowscriptaccess" value="always"></param>
        <embed src="%(link)s" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="480" height="385"></embed>
    </object>
    <p>date: %(created_time)s</p>
</div>"""
        vid_list = "<br/>".join(
            [html_unit % vid for vid in vids]
        )

        if user:
            if user.is_active:
                auth.login(request, user)
                # return HttpResponseRedirect('/yay/')
            else:
                error = 'AUTH_DISABLED'
        else:
            error = 'AUTH_FAILED'
    elif 'error_reason' in request.GET:
        error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error, 'vids': vid_list}
    return render_to_response('login.html', template_context, context_instance=RequestContext(request))