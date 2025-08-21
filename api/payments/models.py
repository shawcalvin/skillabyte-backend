from django.db import models

from api.users.models import User
from api.courses.models import Course

class Product(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.price for item in self.cart_items)

    def add_item(self, product):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)

        if created:
            cart_item.save()
            return cart_item

    def remove_item(self, product):
        try:
            cart_item = self.cart_items.get(product=product).delete()
            return cart_item
        
        except CartItem.DoesNotExist:
            return None

    def clear(self):
        self.delete()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'cart'], name='unique_cart_product')
        ]


class PaymentStatus(models.Model):
    status = models.CharField(max_length=64, unique=True)


class Currency(models.Model):
    status = models.CharField(max_length=3, unique=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    session_id = models.CharField(max_length=128)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, null=True, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'order'], name='unique_order_product')
        ]