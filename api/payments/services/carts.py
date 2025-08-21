from ..models import Cart

class CartService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CartService, cls).__new__(cls)
        return cls._instance
    
    def clear_cart(self, user):
        cart = Cart.objects.get(user=user)        
        cart.clear()