from provider.facebook import FacebookProvider

providers = {
    'facebook': FacebookProvider
}


def get_provider(provider):
    if provider in providers:
        return providers[provider]
    else:
        raise NotImplementedError('no provider named "%s"') % provider