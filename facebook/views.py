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

    ctx = {}

    # import ipdb; ipdb.set_trace()
    if data.get('oauth_token'):
        graph = fb_sdk.GraphAPI(data['oauth_token'])
        # fb_info = graph.get_object('me', fields='name,location')

        def iter_links(results):
            for r in results:
                attachment = r['attachment']
                media_list = attachment.get('media')
                if media_list:
                    for media in media_list:
                        href = media.get('href')
                        if href and 'youtube' in href:
                            yield href

        json_results = graph.fql('SELECT attachment.media FROM stream WHERE filter_key="nf" LIMIT 50')
        sources = set(iter_links(json_results))
        ctx['youtubes'] = simplejson.dumps(tuple(sources))
    else:
        ctx['pending_fb_authorization'] = True

    return render_to_response('canvas.html', ctx, context_instance=RequestContext(request))
