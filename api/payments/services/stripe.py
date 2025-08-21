from django.conf import settings

import stripe
import stripe.error

from .orders import OrderService
from .carts import CartService
from ..models import Order, Product, PaymentStatus, Currency

from api.users.models import User
from api.organizations.services.organizations import OrganizationService

class StripeService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StripeService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.base_domain = settings.BASE_FRONTEND_DOMAIN
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_line_item(self, product_name, product_description, unit_amount, currency='usd', quantity=1):
        return { 'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': product_name,
                            'description': product_description,
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': quantity,
                }

    def create_checkout_session(self, user, line_items, success_url, cancel_url, mode='payment'):
        return stripe.checkout.Session.create(
            customer_email = user.email,
            line_items = line_items,
            allow_promotion_codes=True,
            success_url = self.base_domain + success_url,
            cancel_url = self.base_domain + cancel_url,
            mode=mode
        )
    
    def construct_webhook_event(self, payload, header):
        return stripe.Webhook.construct_event(
                payload, header, self.webhook_secret
        )

    def handle_webhook_event(self, event):
        if event['type'] == 'checkout.session.completed':
            return self.handle_checkout_event(event)
        else:
            return {'message': 'Webhook event ignored.'}

    def handle_checkout_event(self, event):
        order_service = OrderService()
        organization_service = OrganizationService()
        cart_service = CartService()
        
        session = event.data.object
        user_email=session['customer_details']['email']

        user = User.objects.get(email=user_email)
        organization = organization_service.get_personal_organization(user=user)

        if session['payment_status'] != 'paid':
            return {'error': 'Payment not completed'}

        line_items = stripe.checkout.Session.list_line_items(session['id'])
        
        try:
            line_items = stripe.checkout.Session.list_line_items(session['id'])
        except stripe.error.StripeError as e:
            return {'error': str(e)}
        
        purchased_items = []
        for item in line_items['data']:
            purchased_items.append({
                'product_name': item['description'],
                'quantity': item['quantity'],
                'price': item['amount_total'] / 100,
                'currency': item['currency'],
            })

        try:
            order = order_service.create_order(
                user=user,
                session_id=session['id'],
                payment_status=PaymentStatus.objects.filter(status=session['payment_status']).first(),
                amount=session['amount_total'] / 100,
                currency=Currency.objects.filter(status=session['currency']).first()
            )

            for item in purchased_items:
                product = Product.objects.get(course__title=item['product_name'])
                order_service.create_order_item(
                    order=order,
                    product=product
                )
            
                organization_service.add_course_to_organization(
                    organization=organization,
                    course=product.course
                )

            cart_service.clear_cart(user)

            return {'message': 'Order processed successfully'}
        
        except Exception as e:
            return {'error': str(e)}