def includeme(config):
    config.add_route('pyramid-social-auth.auth', '/psa/login/{provider}')
    config.add_route('social.complete', '/psa/complete/{backend}')