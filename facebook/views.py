from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.conf import settings

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
        return HttpResponse(simplejson.dumps(tuple(vids)))
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

# TODO perhaps this is entirely unnecessarry
# TODO look into doing the decoding using oauth2 module
import socialregistration.facebook as fb_sdk
from utils import iterytlinks
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
        fb_info = {
            'FACEBOOK_APP_NAME': settings.FACEBOOK_APP_NAME,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
        }
        return render_to_response('canvas_authorize.html', fb_info, context_instance=RequestContext(request))

    graph = fb_sdk.GraphAPI(data['oauth_token'])
    # fb_info = graph.get_object('me', fields='name,location')

    json_results = graph.fql('SELECT attachment.media FROM stream WHERE filter_key="nf" LIMIT 100')
    sources = set(iterytlinks(json_results))
    ctx = dict(youtubes=simplejson.dumps(tuple(sources)))
    return render_to_response('canvas.html', ctx, context_instance=RequestContext(request))
