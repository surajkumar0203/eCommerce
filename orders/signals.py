from django.dispatch import receiver
from django.db.models.signals import post_save
from orders.utils import get_orderItem_details
from orders.models import OrderItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=OrderItem)
def order_status_handler(sender,instance,created, **kwargs):
    try:
        if not created:
            channel_layer=get_channel_layer()
            data = get_orderItem_details(instance.slug)
            async_to_sync(channel_layer.group_send)(
                f'order_progress_{instance.slug}',
                {
                    'type':'order.status',
                    'value':data
                }
            
            )
       
    except Exception as e:
        pass