from provider.base import BaseProvider
from nose.tools import eq_, ok_


class TestBaseProvider():
    def test_base_init(self):
        base = BaseProvider('client_id', 'client_secret', 'authorize_url', 'access_token_url', 'base_url', 'name', 'redirect_uri', state='test')
        eq_(base.settings['client_id'], 'client_id')
        eq_(base.settings['client_secret'], 'client_secret')
        eq_(base.settings['authorize_url'], 'authorize_url')
        eq_(base.settings['access_token_url'], 'access_token_url')
        eq_(base.settings['base_url'], 'base_url')
        eq_(base.settings['name'], 'name')
        eq_(base.settings['redirect_uri'], 'redirect_uri')
        eq_(base.settings['state'], 'test')
        
    def test_base_init_no_state(self):
        base = BaseProvider('client_id', 'client_secret', 'authorize_url', 'access_token_url', 'base_url', 'name', 'redirect_uri')

        ok_(base.settings['state'] is None)

    def test_do_no_mutate_state(self):
        base = BaseProvider('client_id', 'client_secret', 'authorize_url', 'access_token_url', 'base_url', 'name', 'redirect_uri', state='test')
        eq_(base.get_state(), 'test')
    
    def test_mutate_state(self):
        base = BaseProvider('client_id', 'client_secret', 'authorize_url', 'access_token_url', 'base_url', 'name', 'redirect_uri')
        
        ok_(base.get_state() is not None)
        ok_(base.settings['state'] is not None)