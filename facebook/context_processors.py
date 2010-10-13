from django.conf import settings

def facebook_info(request):
    facebook = getattr(request, 'facebook', None)
    if facebook and facebook.uid:
        fb_profile = facebook.graph.get_object('me')
    else:
        fb_profile = 'None'
    return {'FBUID': fb_profile}

def facebook_app_info(request):
    return {
        'FACEBOOK_APP_NAME': settings.FACEBOOK_APP_NAME,
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
    }