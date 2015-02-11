import unittest
from urllib.parse import urlparse, parse_qs
from pyramid.httpexceptions import HTTPFound
from pyramid.registry import Registry
from pyramid.testing import DummyRequest, testConfig
from pyramid_app.views import auth


class TestViewAuth(unittest.TestCase):
    def test_facebook(self):
        registry = Registry()
        
        with testConfig(registry=registry) as config:
            config.registry.settings.update({
                'facebook': {
                    'client_id': 'abc',
                    'client_secret': 'def'
                },
                'application_name': 'test'
            })
            
            config.add_route('pyramid-social-auth.complete', '/psa/complete/{provider}')
            request = DummyRequest()
            request.matchdict = {'provider': 'facebook'}
    
            response = auth(request)
    
            assert isinstance(response, HTTPFound)
            
            facebook_url = urlparse(response.location)
            
            assert facebook_url.scheme == 'https'
            assert facebook_url.netloc == 'www.facebook.com'
            assert facebook_url.path == '/dialog/oauth'
            
            query = parse_qs(facebook_url.query)

            assert query['scope'][0] == 'email public_profile'
            assert query['response_type'][0] == 'code'
            assert query['redirect_uri'][0] == 'http://example.com/psa/complete/facebook'
            assert query['client_id'][0] == 'abc'
            assert query['state'][0] == '0123456789012345678901234567890123456789'
            assert query['duration'][0] == 'permanent'