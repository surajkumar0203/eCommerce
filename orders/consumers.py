from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from orders.utils import get_orderItem_details

class OrderTrack(WebsocketConsumer):
    def connect(self):
        self.room_slug=self.scope['url_route']['kwargs']['track_id']
        self.room_group_name = f'order_progress_{self.room_slug}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )   
        order_item=get_orderItem_details(slug=self.room_slug)
        self.accept()
        self.send(text_data=json.dumps({"payload": order_item}))


    def order_status(self,event):
        data=event["value"]
        self.send(text_data=json.dumps({"payload": data}))
        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )
        