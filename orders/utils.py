from orders.models import OrderItem



def get_orderItem_details(slug):
    order_mapper={
        'Order Received':20,
        'Order Packed':40,
        'Order Shipped':60,
        'Out Of Delivery':80,
        'Order Delivered':100
    }
    try:
        order_item=OrderItem.objects.get(slug=slug)
        return {
            'status':order_item.status,
            'progress_percentage':order_mapper[order_item.status]
        }
    except OrderItem.DoesNotExist:
        return "Order not found"