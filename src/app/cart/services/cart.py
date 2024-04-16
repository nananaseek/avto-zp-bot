from typing import Dict, List, Optional

from src.core.database.redis.connect import cart


class CartService:
    _CART_SESSION = cart
    _EXPIRED_TIME = 60 * 60

    async def save_cart(self, **kwargs) -> bool:
        # check if cart already exists
        user_id = kwargs['user_id']
        uuid_id = kwargs['id']
        key = f"carts:{user_id}:{uuid_id}"

        async for user_carts in self._CART_SESSION.scan_iter(f"carts:{user_id}:*"):
            data = await self._get_all_carts_data(user_carts)

            if int(data['user_id']) == int(user_id) and str(data['id']) == str(uuid_id):
                await self._update_time_all_cart(data=data)

                if int(data['takes_by_user']) >= int(data['quantity']):
                    return False
                else:
                    await self._CART_SESSION.hincrby(
                        f'carts:{data['user_id']}:{data['id']}',
                        'takes_by_user'
                    )
                    return True

        [await self._CART_SESSION.hset(key, index, str(value)) for index, value in kwargs.items()]
        await self._CART_SESSION.expire(key, self._EXPIRED_TIME)

        return True

    async def _quantity_check(self, data: dict) -> bool:
        if int(data['takes_by_user']) >= int(data['quantity']):
            return False
        else:
            await self._CART_SESSION.hincrby(
                f'carts:{data['user_id']}:{data['id']}',
                'takes_by_user'
            )
            return True

    async def _get_all_carts_data(self, user_carts: dict) -> dict:
        items = await self._CART_SESSION.hgetall(user_carts)
        data = {
            index.decode('utf-8'): value.decode('utf-8') for index, value in items.items()
        }
        return data

    async def _update_time_all_cart(self, data: dict = None) -> None:
        if data is not None:
            await self._CART_SESSION.expire(
                f'carts:{data['user_id']}:{data['id']}',
                self._EXPIRED_TIME
            )

    async def carts(self, user_id: int) -> List[Dict[str, str]]:
        description = []

        async for user_carts in self._CART_SESSION.scan_iter(f"carts:{user_id}:*"):
            data = await self._get_all_carts_data(user_carts)
            await self._update_time_all_cart(data)

            if int(data['takes_by_user']) > 1:
                items_price = float(data['price']) * float(data['takes_by_user'])
            else:
                items_price = float(data['price'])

            data.update(items_price=items_price)
            description.append(data)
        return description

    async def get_product_from_cart(self, user_id: int, uuid: str) -> Optional[dict]:
        key = f"carts:{user_id}:{uuid}"
        item = await self._CART_SESSION.hgetall(key)
        if len(item) > 0:
            product = {index.decode('utf-8'): value.decode('utf-8') for index, value in item.items()}
        else:
            product = None
        return product

    async def add_product_to_cart(self, user_id: int, uuid: str, amount: int = 1) -> Optional[bool]:
        data = await self.get_product_from_cart(user_id=user_id, uuid=uuid)
        if data is None:
            return None
        else:
            if amount + int(data['takes_by_user']) > int(data['quantity']):
                return False
            else:
                await self._CART_SESSION.hincrby(
                    f'carts:{data['user_id']}:{data['id']}',
                    'takes_by_user',
                    amount=amount
                )
                return True

    async def add_choose_amount(self, user_id: int, uuid: str, amount: int) -> Optional[bool]:
        data = await self.get_product_from_cart(user_id=user_id, uuid=uuid)
        if data is None:
            return None
        else:
            takes_by_user = int(data['takes_by_user'])
            quantity = int(data['quantity'])
            if takes_by_user >= quantity and amount + takes_by_user > data['quantity']:
                return False
            else:
                await self._CART_SESSION.hincrby(
                    f'carts:{data['user_id']}:{data['id']}',
                    'takes_by_user'
                )
                return True

    async def delete_product_cart(self, user_id: int, uuid: str) -> Optional[bool]:
        data = await self.get_product_from_cart(user_id=user_id, uuid=uuid)
        if data is None:
            return None
        else:
            if int(data['takes_by_user']) <= 1:
                await self._CART_SESSION.delete(f"carts:{data['user_id']}:{data['id']}")
                return True
            else:
                await self._CART_SESSION.hincrby(
                    f'carts:{data['user_id']}:{data['id']}',
                    'takes_by_user',
                    amount=-1
                )
                return False

    async def delete_all_carts(self, user_id: int) -> None:
        [await self._CART_SESSION.delete(x) async for x in self._CART_SESSION.scan_iter(f"carts:{user_id}:*")]


cart_service = CartService()
