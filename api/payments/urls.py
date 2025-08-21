from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path("checkout/", views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path("success/", views.StripeWebhookHandlerView.as_view(), name="webhook"),
    path("cart/", views.CartDetailView.as_view(), name="cart"),
    path("cart/add/", views.CartAddItemView.as_view(), name="cart_add"),
    path("cart/remove/", views.CartRemoveItemView.as_view(), name="cart_add"),
    path("cart/clear/", views.CartClearItemsView.as_view(), name="cart_clear"),
]