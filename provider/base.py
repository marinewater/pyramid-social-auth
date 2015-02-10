from collections import defaultdict
import json
from rauth import OAuth2Service
import random
import string


class BaseProvider():
    def __init__(self, client_id, client_secret, authorize_url, access_token_url, base_url, name, redirect_uri,
                 state=None):
        self.settings = {
            'client_id': client_id,
            'client_secret': client_secret,
            'authorize_url': authorize_url,
            'access_token_url': access_token_url,
            'base_url': base_url,
            'name': name,
            'redirect_uri': redirect_uri,
            'state': state
        }

        self.headers = {
            'User-Agent': 'pyramid-social-auth/0.0.0'  # some providers are rate limited against user agents
        }

        self.session = None
        self.info = defaultdict(None)

        self.service = OAuth2Service(
            client_id=self.settings['client_id'],
            client_secret=self.settings['client_secret'],
            name=self.settings['name'],
            authorize_url=self.settings['authorize_url'],
            access_token_url=self.settings['access_token_url'],
            base_url=self.settings['base_url']
        )

    def auth(self, scope=None):
        params = {'redirect_uri': self.settings['redirect_uri'],
                  'duration': 'permanent',
                  'response_type': 'code',
                  'state': self.get_state()}
        
        if scope is not None:
            params['scope'] = scope

        url = self.service.get_authorize_url(**params)

        return url

    def get_state(self):
        if self.settings['state'] is None:
            self.settings['state'] = ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
        return self.settings['state']

    def get_session(self, code, state=None):
        """

        :param state: a random string to prevent csrf attacks, must match the one used in self.auth()
        :param code: the code provided by the OAuth2 provider if the authorization is successful
        """
        data = {
            'grant_type': "authorization_code",
            'code': code,
            'redirect_uri': self.settings['setredirect_uri']
        }
        if state is not None:
            data['state'] = state

        self.session = self.service.get_auth_session(
            auth=(self.settings['client_id'], self.settings['client_secret']),
            data=data,
            headers=self.headers,
            decoder=lambda b: json.loads(b.decode(encoding='UTF-8')))  # rauth apparently cannot handle bytes

    def get_auth_token(self):
        if self.session is None:
            raise AttributeError
        else:
            return self.session.access_token

    def get_info(self, path):
        """

        :param path: path for api resource
        :return: :rtype: dict
        """
        if self.session is None:
            raise AttributeError
        else:
            return self.session.get(path, bearer_auth=True, headers=self.headers).json()

    def get_user_info(self, info):
        """
        retrieve basic user info

        """
        raise NotImplementedError('Implement get_user_info in subclass')

    def get_user(self):
        """
        retrieve username
        :return: :rtype: string
        """
        raise NotImplementedError('Implement get_user in subclass')

    def get_email(self):
        """
        retrieve users email address
        :return: :rtype: string
        """
        raise NotImplementedError('Implement get_email in subclass')