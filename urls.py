from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^$', 'facebook.views.login'),
    (r'^youtubes/$', 'facebook.views.youtube_vids'),
    (r'^youtubezzz/$', 'facebook.views.youtube_vids_stub'),

    # for andrey
    (r'^player/$', 'django.views.generic.simple.direct_to_template', {'template': 'ytplayer.html'}),
    
    # media
    (r'^statics/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
