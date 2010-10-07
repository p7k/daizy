from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^$', 'facebook.views.login'),
    (r'^youtubes/$', 'facebook.views.youtube_vids'),
    (r'^youtubezzz/$', 'facebook.views.youtube_vids_stub'),

    # for andrey
    (r'^player/$', 'django.views.generic.simple.direct_to_template', {'template': 'ytplayer.html'}),

    # 960
    (r'^index/$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    
    # media
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^facebook/', include('django_facebook.urls')),
)
