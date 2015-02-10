from pyramid.view import view_config

@view_config(route_name='pyramid-social-auth.auth', request_method='GET')
def auth(request):
    pass