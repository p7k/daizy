from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^social/', include('socialregistration.urls')),

    (r'^youtubes/$', 'facebook.views.youtube_vids'),
    (r'^youtubezzz/$', 'facebook.views.youtube_vids_stub'),    

    (r'^player/$', 'facebook.views.player'),
    (r'^canvas/$', 'facebook.views.canvas'),

    # 960
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    
    # media
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
