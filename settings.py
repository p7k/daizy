try:
    from djangoappengine.settings_base import *
    has_djangoappengine = True
except ImportError:
    has_djangoappengine = False
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

import os

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
)

# if has_djangoappengine:
#     INSTALLED_APPS = ('djangoappengine',) + INSTALLED_APPS

TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

# Activate django-dbindexer if available
try:
    import dbindexer
    DATABASES['native'] = DATABASES['default']
    DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
    INSTALLED_APPS += ('dbindexer',)
except ImportError:
    pass

#################################################################
#########################  MY SETTINGS  #########################
#################################################################
from django.conf import settings
if has_djangoappengine:
    from djangoappengine.utils import on_production_server
else:
    on_production_server = False

# Media
MEDIA_URL = '/static/'

# Facebook via socialregistration
INSTALLED_APPS += (
    'facebook',
    'socialregistration'
)
AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS + (
    'socialregistration.auth.FacebookAuth',
)
MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + (
    'socialregistration.middleware.FacebookMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

if on_production_server:
    FACEBOOK_APP_ID = '143155229062210'
    FACEBOOK_API_KEY = 'b8887dfe5ade767643db465d9d6aaae1'
    FACEBOOK_APP_SECRET = 'a6371309726429fabc5bb7a469644b22'
else:
    FACEBOOK_APP_ID = '113435098718000'
    FACEBOOK_API_KEY = '852482d9db128f355cc891748300642b'
    FACEBOOK_APP_SECRET = '50e2c8bc51fcc45926ba84c772b4ef43'
FACEBOOK_SECRET_KEY = FACEBOOK_APP_SECRET

SITE_ID = 3