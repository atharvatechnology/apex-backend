from .factory import ProviderFactory
from .zoom.meet import ZoomProvider

provider_factory = ProviderFactory()

provider_factory.register_provider("zoom", ZoomProvider)
