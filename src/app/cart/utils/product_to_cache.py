from src.app.cart.services.cart import cart_service
from src.app.product.services.product import product_service


async def get_product_to_cache(product_id: str, user_id: int) -> bool:
    product = await product_service.get(id=product_id)

    if product.discount is None:
        is_discount = product.price
        product.discount = 0
    else:
        is_discount = product.price - (product.price * product.discount / 100)

    to_cart = {
        'user_id': user_id,
        'id': product.id,
        'image': product.image,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'discount': product.discount,
        'new_price': is_discount,
        'quantity': product.quantity,
        'takes_by_user': 1
    }

    return await cart_service.save_cart(**to_cart)
