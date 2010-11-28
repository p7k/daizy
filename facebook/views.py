from itertools import imap, ifilter

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings

from djangotoolbox.http import JSONResponse
from socialregistration.models import FacebookProfile
import socialregistration.facebook as fb_sdk
from utils import fb_account_setup, now_timestamp, fql_query, skinny_video_post


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
        return render_to_response('canvas_authorize.html', context_instance=RequestContext(request))

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

    return render_to_response('canvas.html', context_instance=RequestContext(request))


@login_required
def videos_increment(request, limit=30):
    graph = fb_sdk.GraphAPI(request.session['oauth_token'])
    sources = []
    # always return at least two to avoid 
    while len(sources) < 2:
        timestamp = request.session.get('facebook_timestamp', now_timestamp())
        fql = fql_query(timestamp, limit=limit)
        # import ipdb; ipdb.set_trace()
        # TODO secure this call with some exception handling + timeout
        json_results = graph.fql(fql)
        if not json_results: break
        request.session['facebook_timestamp'] = json_results[-1]['created_time']
        video_posts = imap(skinny_video_post, json_results)
        sources += list(ifilter(None, video_posts))
    return JSONResponse(sources)
