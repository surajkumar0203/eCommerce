from datetime import datetime
from uuid import uuid4

def generate_order_id(item_count):
    now= datetime.now()
    item_count=str(item_count).zfill(4)
    order_id = f"ORD-{now.strftime("%Y%m%d-%H%M%S")}-{item_count}"
    return order_id


# generate slug for orderItem

def generate_slug(order_id):
    order_id=str(order_id)
    order_id=order_id.split("-")
    unique=str(uuid4()).split("-")[0]
    return "".join([order_id[1],order_id[2],unique])
    