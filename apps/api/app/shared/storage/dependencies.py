from .factory import get_storage

def get_restaurant_storage():
    return get_storage("restaurants")

def get_product_storage():
    return get_storage("dishes")