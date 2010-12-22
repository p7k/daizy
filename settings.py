# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'djangotoolbox',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

# Activate django-dbindexer if available
try:
    # import dbindexer
    DATABASES['native'] = DATABASES['default']
    DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
    INSTALLED_APPS += ('dbindexer',)
except ImportError:
    pass

#################################################################
#########################  MY SETTINGS  #########################
#################################################################
INSTALLED_APPS += (
    'socialregistration',
    'facebook',
)

# does it have to be this difficult to extend the damn settings?
from django.conf.global_settings import AUTHENTICATION_BACKENDS, MIDDLEWARE_CLASSES, TEMPLATE_CONTEXT_PROCESSORS
AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
    'socialregistration.auth.FacebookAuth',
)
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'socialregistration.middleware.FacebookMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'facebook.context_processors.facebook_info',
    'facebook.context_processors.facebook_app_info',
)

SOCIALREGISTRATION_GENERATE_USERNAME = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

if on_production_server:
    SITE_ID = 2
    FACEBOOK_APP_NAME = 'daizytv'
    FACEBOOK_APP_ID = '143155229062210'
    FACEBOOK_API_KEY = 'b8887dfe5ade767643db465d9d6aaae1'
    FACEBOOK_SECRET_KEY = 'a6371309726429fabc5bb7a469644b22'
else:
    SITE_ID = 1
    FACEBOOK_APP_NAME = 'daizy_test'
    FACEBOOK_APP_ID = '113435098718000'
    FACEBOOK_API_KEY = '852482d9db128f355cc891748300642b'
    FACEBOOK_SECRET_KEY = '50e2c8bc51fcc45926ba84c772b4ef43'
