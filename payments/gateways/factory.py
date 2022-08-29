class GatewayFactory:
    def __init__(self):
        self._gateways = {}

    def register_gateway(self, key, gateway):
        self._gateways[key] = gateway

    def get_gateway(self, key, **kwargs):
        gateway = self._gateways.get(key)
        if not gateway:
            raise ValueError("{} is not registered.".format(key))
        return gateway(**kwargs)

    def get_gateways(self):
        return self._gateways.keys()
