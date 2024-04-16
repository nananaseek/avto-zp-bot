from typing import Dict, List

from src.core.database.redis.connect import check


class OrderService:
    _ORDER_SESSION = check
    _EXPIRED_TIME = 60 * 60 * 24 * 7

    async def save_check(self, **kwargs):
        user_id = kwargs['user_id']

        async for _ in self._ORDER_SESSION.scan_iter(f"check:{user_id}:*"):
            kwargs['check_id'] += 1

        check_id = kwargs['check_id']
        key = f"check:{user_id}:{check_id}"

        [await self._ORDER_SESSION.hset(key, index, str(value)) for index, value in kwargs.items()]
        await self._ORDER_SESSION.expire(key, self._EXPIRED_TIME)

    async def get_all_user_orders(self) -> List[Dict]:
        orders = []
        async for order in self._ORDER_SESSION.scan_iter(f"check:*"):
            data = await self._get_order(order)
            orders.append(data)
        return orders

    async def _get_order(self, order_key: str) -> dict:
        items = await self._ORDER_SESSION.hgetall(order_key)
        data = {
            index.decode('utf-8'): value.decode('utf-8') for index, value in items.items()
        }
        return data

    async def get_target_user_order(self, user_id: int, check_id: int) -> dict:
        key = f"check:{user_id}:{check_id}"
        return await self._get_order(key)

    async def delete_user_order(self, user_id: int, check_id: int) -> dict:
        key = f"check:{user_id}:{check_id}"
        return await self._ORDER_SESSION.delete(key)


order_service = OrderService()
