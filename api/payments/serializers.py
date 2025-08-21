from rest_framework import serializers

from .models import Cart, CartItem, Product
from api.courses.serializers import CourseSerializer

class PaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True, min_value=1)
    currency = serializers.CharField(required=True, max_length=3)

    def validate_currency(self, value):
        if value.upper() not in ['USD']:
            raise serializers.ValidationError("Unsupported currency.")
        return value
    

class ProductSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Product
        fields = ['id', 'course', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user']