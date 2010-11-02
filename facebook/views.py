from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings
from djangotoolbox.http import JSONResponse
from socialregistration.models import FacebookProfile
from time import mktime
from datetime import datetime

@login_required
def player(request):
    return render_to_response('ytplayer.html', context_instance=RequestContext(request))

@login_required
def youtube_vids(request):
    facebook = getattr(request, 'facebook', None)
    if facebook and facebook.uid:
        def home_feed():
            return facebook.graph.get_connections('me', 'home', fields='from,link', limit=100)
        def yt_link_filter(result):
            link = result.get('link')
            return True if link and 'youtube' in link else False
        vids = (r for r in home_feed()['data'] if yt_link_filter(r))
        return JSONResponse(tuple(vids))
    else:
        return HttpResponseServerError('not facebook authenticated')

def youtube_vids_stub(request):
    return JSONResponse([
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
    ])

# TODO perhaps this is entirely unnecessarry
# TODO look into doing the decoding using oauth2 module
import socialregistration.facebook as fb_sdk
def canvas(request):
    """services facebook canvas"""
    signed_request = request.GET.get('signed_request')

    # redirect early if not from facebook
    if not signed_request:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    # process signed_request if from facebook
    data = fb_sdk.parse_signed_request(signed_request)

    # TODO should prolly be a server error or something like that
    if not data:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    oauth_token = data.get('oauth_token')

    # request authorization / extended permissions
    if not oauth_token:
        return render_to_response('canvas_authorize.html', {
            'FACEBOOK_APP_NAME': settings.FACEBOOK_APP_NAME,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
        }, context_instance=RequestContext(request))

    # authentication / start session
    uid = data.get('user_id')
    user = authenticate(uid=uid)

    if user:
        login(request, user)
    else:
        user = User()
        facebook_profile = FacebookProfile(uid=uid)
        fb_account_setup(request, user, facebook_profile)

    request.session['oauth_token'] = oauth_token
    
    if request.session.has_key('facebook_timestamp'):
        del request.session['facebook_timestamp']

    # fb_info = graph.get_object('me', fields='name,location')
    return render_to_response('canvas.html', context_instance=RequestContext(request))

import uuid
from socialregistration.forms import UserForm
def fb_account_setup(request, user, facebook_profile):
    form = UserForm(user, facebook_profile)
    if form.is_valid():
        form.save(request=request)
        user = form.profile.authenticate()
        login(request, user)
    else:
        # Generate user and profile
        user.username = str(uuid.uuid4())[:30]
        user.save()

        facebook_profile.user = user
        facebook_profile.save()

        # Authenticate and login
        user = facebook_profile.authenticate()
        login(request, user)


def fql_query(uid, timestamp, limit):
    # TODO look into filtering (WHERE filter_key="nf")
    return 'SELECT %(stream_fields)s FROM stream WHERE source_id IN (SELECT target_id FROM connection WHERE source_id = %(uid)i) AND is_hidden = 0 AND created_time < %(timestamp)i LIMIT %(limit)i' % {
        'stream_fields': "post_id, attachment.media, created_time, permalink",
        'uid': int(uid),
        'timestamp': int(timestamp),
        'limit': int(limit)
    }

from utils import iter_prep_posts
now_timestamp = lambda: mktime(datetime.now().timetuple())
@login_required
def youtube_increment(request, limit=30):
    graph = fb_sdk.GraphAPI(request.session['oauth_token'])
    facebook_profile = FacebookProfile.objects.get(user=request.user)
    sources = None
    while not sources:
        timestamp = request.session.get('facebook_timestamp', now_timestamp())
        fql = fql_query(facebook_profile.uid, timestamp, limit)
        json_results = graph.fql(fql)
        if not json_results: break
        request.session['facebook_timestamp'] = json_results[-1]['created_time']
        sources = tuple(iter_prep_posts(json_results))
    return JSONResponse(sources)
