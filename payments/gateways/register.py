from .esewa.pay import EsewaGateway
from .factory import GatewayFactory

# from .khalti.pay import KhaltiGateway

gateway_factory = GatewayFactory()

gateway_factory.register_gateway("esewa", EsewaGateway)
# gateway_factory.register_gateway('khalti', EsewaGateway)
