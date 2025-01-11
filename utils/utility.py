from datetime import datetime

def generate_order_id(item_count):
    now= datetime.now()
    item_count=str(item_count).zfill(4)
    order_id = f"ORD-{now.strftime("%Y%m%d-%H%M%S")}-{item_count}"
    return order_id