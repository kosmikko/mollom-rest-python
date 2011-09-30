import urllib

from google.appengine.api import urlfetch

import oauth
from oauth.signature_method.hmac_sha1 import OAuthSignatureMethod_HMAC_SHA1

class MollomRequest(object):
    API_URL = 'http://rest.mollom.com/v1/'
    # mollom public API key
    CONSUMER_KEY = 'xx'
    # mollom private API key
    CONSUMER_SECRET = 'xx'

    def api_request(self, url, http_method='GET', post_data=None):
        """
        Params:
        url - relative url, e.g. 'content'
        post_data - dict of POST parameters
        """
        params_list = encoded_params = None
        url = "%s%s" % (self.API_URL, url)
        if post_data:
            encoded_params = self.url_encode_params(post_data)

        consumer = {'oauth_token': self.CONSUMER_KEY, 'oauth_token_secret': self.CONSUMER_SECRET}
        request = oauth.OAuthRequest(url, http_method='POST', params=encoded_params)
        request.sign_request(OAuthSignatureMethod_HMAC_SHA1, consumer)
        headers = {'Authorization': request.to_header(),
                   'Accept': 'application/json;q=0.8, */*;q=0.5'}

        result = urlfetch.fetch(url,
                                payload=None if post_data is None else encoded_params,
                                method=urlfetch.GET if request.http_method == "GET" else urlfetch.POST,
                                headers=headers,
                                )

        if result.status_code == 200:
            return result.content

        raise RuntimeError("fail to access resource, status=%d, url=%s, %s" % (result.status_code, url, result.content))

    def url_encode_params(self, params):
        if not isinstance(params, dict): 
            raise NotImplementedError("You must pass in a dictionary!")
        params_list = []
        for k,v in params.items():
            # handle multiple parameters with same name, e.g. {'checks': ["spam", "profanity"]}
            if isinstance(v, list): params_list.extend([(k, x) for x in v])
            else: params_list.append((k, v))
        return urllib.urlencode(params_list)