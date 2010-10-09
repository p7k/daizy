def facebook_info(request):
    facebook = getattr(request, 'facebook', None)
    if facebook and facebook.uid:
        fb_profile = facebook.graph.get_object('me')
    else:
        fb_profile = 'None'
    return {'FBUID': fb_profile}