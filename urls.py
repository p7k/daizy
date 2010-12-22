from django.conf import settings
from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),

    # ('^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
    (r'^admin/', include(admin.site.urls)),

    (r'^social/', include('socialregistration.urls')),

    (r'^canvas/$', 'facebook.views.canvas'),
    (r'^videos/$', 'facebook.views.videos_increment'),

    # 960
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    # media
    # (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0]}),

    # testing only
    (r'^jw/$', 'django.views.generic.simple.direct_to_template', {'template': 'jwplayer.html'}),
)
