import stripe
from stripe import Product, Price, checkout

from config.settings import STRIPE_SECRET_KEY


stripe.api_key = STRIPE_SECRET_KEY

def create_product(title):
    return Product.create(name=title).get('id')

def create_price(obj):
    return Price.create(
        currency="RUB",
        unit_amount=obj.price * 100,
        product=create_product(obj.title)
    ).get('id')

def create_session(course):
    return checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": create_price(course), "quantity": 1}],

            mode="payment",
        )

def session_retrieve(session_id):
    return stripe.checkout.Session.retrieve(session_id)
