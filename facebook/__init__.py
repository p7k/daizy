from facebook_sdk import *

import hashlib
import hmac
import base64

from django.utils import simplejson
from django.conf import settings

class GraphAPI(GraphAPI):
    """extending the SDK for work with FQL"""
    def fql(self, query, format='json'):
        # post_data = dict(oauth_token=data['oauth_token'])
        params = urllib.urlencode(dict(
            query=query,
            format=format,
            oauth_token=self.access_token
        ))
        url = '?'.join(('https://api.facebook.com/method/fql.query', params))
        # response = urllib.urlopen(url, post_data)
        response = urllib.urlopen(url)
        return simplejson.loads(response.read())

def _base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret=settings.FACEBOOK_SECRET_KEY):
    encoded_sig, payload = signed_request.split('.', 2)
    sig = _base64_url_decode(encoded_sig)
    data = simplejson.loads(_base64_url_decode(payload))
    # return if incorrect algorithm is use
    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()
    return data if sig == expected_sig else None
