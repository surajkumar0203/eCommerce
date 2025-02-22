from django.urls import path
from orders.consumers import OrderTrack

ws_urlrouter=[
    path("ws/order/<track_id>/", OrderTrack.as_asgi()),
]