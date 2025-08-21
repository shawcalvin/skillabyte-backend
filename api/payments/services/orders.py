
from ..models import Order, OrderItem

class OrderService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrderService, cls).__new__(cls)
        return cls._instance
    
    def create_order(self, user, session_id, payment_status, amount, currency):
        return Order.objects.create(
                user=user,
                session_id=session_id,
                payment_status=payment_status,
                amount=amount,
                currency=currency
        )

    def create_order_item(self, order, product):
        return order.order_items.create(
            product=product
        )