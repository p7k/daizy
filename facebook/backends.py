from django.conf import settings
from django.contrib.auth.models import User
from django.utils import simplejson

import facebook_sdk as fb

class FacebookBackend:
    def authenticate(self, access_token=None):
        try:
            user = User.objects.get(password=access_token)
        except User.DoesNotExist:
            graph = fb.GraphAPI(access_token)
            profile = graph.get_object('me')
            user = User(username=profile['id'],
                        # email = profile['email'],
                        first_name = profile['first_name'],
                        last_name = profile['last_name'],
                        password=access_token)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None