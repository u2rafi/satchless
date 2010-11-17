from django.conf import settings
from django.utils.importlib import import_module
from satchless.pricing import Price

_processors_queue = None

def get_variant_price(variant, quantity=1, **kwargs):
    price = Price()
    for handler in _processors_queue:
        try:
            price = handler.get_variant_price(variant, quantity=quantity, price=price, **kwargs)
        except StopPropagation:
            break
    return price

def get_product_price_range(product, **kwargs):
    price = Price()
    for handler in _processors_queue:
        try:
            price = handler.get_product_price_range(product, price=price, **kwargs)
        except StopPropagation:
            break
    return price

def get_cartitem_unit_price(cartitem, **kwargs):
    price = Price()
    for handler in _processors_queue:
        try:
            price = handler.get_cartitem_unit_price(cartitem, price=price, **kwargs)
        except StopPropagation:
            break
    return price

def init_queue():
    global _processors_queue
    _processors_queue = []
    for handler in settings.SATCHLESS_PRICING_HANDLERS:
        if isinstance(handler, str):
            mod_name, han_name = handler.rsplit('.', 1)
            module = import_module(mod_name)
            handler = getattr(module, han_name)
        _processors_queue.append(handler)

if _processors_queue is None:
    init_queue()
