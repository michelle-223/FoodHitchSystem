import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import FoodHitchApp.routing  # Adjust to your app’s routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodHitchDelivery.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            FoodHitchApp.routing.websocket_urlpatterns
        )
    ),
})
