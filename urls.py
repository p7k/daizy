from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^$', 'facebook.views.login'),
    (r'^youtubes/$', 'facebook.views.youtube_vids'),

    # for andrey
    (r'^player/$', 'django.views.generic.simple.direct_to_template', {'template': 'ytplayer.html'}),
)
