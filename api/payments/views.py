
from django.shortcuts import get_object_or_404
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets


from .serializers import CartItemSerializer, ProductSerializer
from .models import Product, Cart, CartItem
from .services.stripe import StripeService

from api.organizations.services.organizations import OrganizationService


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            stripe_service = StripeService()

            line_items_data = request.data.get('line_items', [])

            line_items = []
            for item in line_items_data:
                line_items.append(stripe_service.create_line_item(
                    product_name=item.get('name'),
                    product_description=item.get('description'),
                    unit_amount=item.get('unit_price'),
                ))

            checkout_session = stripe_service.create_checkout_session(
                user=user,
                line_items=line_items,
                success_url='/learner/dashboard',
                cancel_url='/learner/payments/cart'
            )

            return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripeWebhookHandlerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        stripe_service = StripeService()

        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        event = stripe_service.construct_webhook_event(
            payload=payload,
            header=sig_header
        )

        response = stripe_service.handle_webhook_event(event=event)

        return Response(response, status=status.HTTP_200_OK)

    
class CartDetailView(APIView):
    def get(self, request, *args, **kwargs):
        items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(items, many=True)

        return Response(serializer.data)


class CartAddItemView(APIView):
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({"course_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST) 
        
        product = Product.objects.get(course__id=course_id)        
        cart, _ = Cart.objects.get_or_create(user=request.user)

        result = cart.add_item(product)
        if not result:
            return Response({"error": "Product already in cart."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Product added to cart."}, status=status.HTTP_200_OK)
    

class CartRemoveItemView(APIView):
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({"course_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST) 
        
        product = Product.objects.get(course__id=course_id)        
        cart = Cart.objects.get(user=request.user)

        result = cart.remove_item(product)
        if not result:
            return Response({"error": "Product not in cart."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
    

class CartClearItemsView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)        
            cart.clear()
            return Response({"message": "Cart cleared."}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is already empty."}, status=status.HTTP_400_BAD_REQUEST)