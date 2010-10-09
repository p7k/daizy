from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^youtubes/$', 'facebook.views.youtube_vids'),
    (r'^youtubezzz/$', 'facebook.views.youtube_vids_stub'),
    
    (r'^', include('socialregistration.urls')),

    # for andrey
    (r'^player/$', 'django.views.generic.simple.direct_to_template', {'template': 'ytplayer.html'}),

    # 960
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    
    # media
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
