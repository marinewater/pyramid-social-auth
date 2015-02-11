from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from provider.utils import get_provider


@view_config(route_name='pyramid-social-auth.auth', request_method='GET')
def auth(request):
    provider_name = request.matchdict.get('provider')

    if provider_name not in request.registry.settings:
        raise LookupError
    
    settings = request.registry.settings[provider_name]

    token = request.session.get_csrf_token()
    provider = get_provider(provider_name)(settings['client_id'], settings['client_secret'],
                                           request.registry.settings['application_name'],
                                           request.route_url('pyramid-social-auth.complete', provider=provider_name),
                                           state=token)

    return HTTPFound(provider.auth())


@view_config(route_name='pyramid-social-auth.complete', request_method='GET')
def complete(request):
    pass