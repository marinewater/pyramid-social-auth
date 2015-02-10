from provider.base import BaseProvider


class FacebookProvider(BaseProvider):
    def __init__(self, client_id, client_secret, name, redirect_uri, state=None):
        """
        
        :param client_id: 
        :param client_secret: 
        :param name: 
        :param redirect_uri: 
        :param state: 
        :return:
        """
        authorize_url = 'https://www.facebook.com/dialog/oauth'
        access_token_url = 'https://graph.facebook.com/oauth/access_token'
        base_url = 'https://graph.facebook.com/'

        super().__init__(self, client_id, client_secret, authorize_url, access_token_url, base_url, name, redirect_uri,
                         state=state)

    def auth(self, scope=None):
        if scope is None:
            scope = 'email public_profile'
        return super().auth(scope)

    def get_user_info(self, info):
        """
        retrieve basic user info

        """
        if self.info[info] is None:
            self.info[info] = self.get_info(info)

    def get_user(self):
        """
        retrieve username
        :return: :rtype: string
        """
        self.get_user_info('me')
        return self.info['me']['name']

    def get_email(self):
        """
        retrieve users email address
        :return: :rtype: string
        """
        self.get_user_info('me')
        return self.info['me']['email']