class ProviderFactory:
    def __init__(self):
        self._providers = {}

    def register_provider(self, key, provider):
        self._providers[key] = provider

    def get_provider(self, key, **kwargs):
        if provider := self._providers.get(key):
            return provider(**kwargs)
        else:
            raise ValueError(f"{key} is not registered.")

    def get_providers(self):
        return self._providers.keys()
