from socialregistration import facebook
from socialregistration import middleware as sr_middleware

class FacebookSR(sr_middleware.Facebook):
    def __init__(self, user=None):
        if user is None:
            self.uid = None
        else:
            self.uid = user['user_id']
            self.user = user
            self.graph = facebook.GraphAPI(user['oauth_token'])

class FacebookMiddleware(sr_middleware.FacebookMiddleware):
    def process_request(self, request):
        """
        Enables ``request.facebook`` and ``request.facebook.graph`` in your views 
        once the user authenticated the  application and connected with facebook. 
        You might want to use this if you don't feel confortable with the 
        javascript library.
        """
        signed_request = request.GET.get('signed_request')

        # redirect early if not from facebook
        if not signed_request:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        # process signed_request if from facebook
        data = fb_sdk.parse_signed_request(signed_request)
        
        
        fb_user = facebook.get_user_from_cookie(request.COOKIES,
            settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)

        request.facebook = Facebook(fb_user)
        
        return None