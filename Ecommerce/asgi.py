

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import orders.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":URLRouter(orders.routing.ws_urlrouter)
})