import logging
from typing import TypeVar

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from pydantic import BaseModel

from src.app.cart.services.cart import cart_service
from src.app.cart.state.cart import ChooseState
from src.app.cart.utils.product_to_cache import get_product_to_cache
from src.core.utils.dell_message import dell_two_message, dell_target_message
from src.core.utils.edit_media import edit_text

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CartWidgets:

    @staticmethod
    async def get_cart(self, user_id: int) -> list:
        return cart_service.carts()

    @staticmethod
    async def add_to_cart(query: CallbackQuery):
        product_id = query.data.split('_')[1]
        user_id = query.from_user.id
        is_add = await get_product_to_cache(product_id, user_id)
        if is_add:
            await query.answer('Товар додано до корзини')
            return True
        else:
            await query.answer(
                'Неможливо додати ще товару бо такої кількості не має на складі'
            )
            return False

    @staticmethod
    async def increase_cart_item(query: CallbackQuery):
        product_id = query.data.split('_')[1]
        is_added = await cart_service.add_product_to_cart(query.from_user.id, product_id, )
        logging.debug(is_added)
        if is_added:
            await query.answer('Одиницю товару додано')
            return True
        if is_added is None:
            is_add = await get_product_to_cache(product_id, query.from_user.id)
            if is_add:
                await query.answer('Товар додано до корзини')
                return True
        else:
            await query.answer('Товар неможливо додати')
            return False

    @staticmethod
    async def choose_amount(query: CallbackQuery, state: FSMContext):
        product_id = query.data.split('_')[1]
        await state.clear()
        await query.message.answer('Скільки ви хочете штук')
        await state.set_state(ChooseState.card_amount)
        await state.update_data(product_id=product_id, message=query.message)

    @staticmethod
    async def decrease_cart_item(query: CallbackQuery):
        product_id = query.data.split('_')[1]
        is_delete = await cart_service.delete_product_cart(query.from_user.id, product_id)
        if is_delete:
            await query.answer('Товар видалено')
            return True
        elif is_delete is None:
            await query.answer('Товару не має в корзині')
            return False
        else:
            await query.answer('Видалено одиницю товару')
            return True

    @staticmethod
    async def get_amount(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            amount = int(message.text)
            data = await state.get_data()
            await edit_text(
                'Добренько:)',
                keyboard=None,
                message_id=message.message_id - 1,
                chat_id=message.chat.id
            )

            product = await cart_service.get_product_from_cart(message.from_user.id, data['product_id'])

            if product is None:
                await message.answer('Помилка, додайте продукт в корзину заново')
                return False
            else:
                is_added = await cart_service.add_product_to_cart(message.from_user.id, data['product_id'],
                                                                  amount=amount)
                if not is_added:
                    await dell_two_message(message.chat.id, message.message_id)
                    await message.answer('Неможливо додати ще товару бо такої кількості не має на складі')
                    return False

            await dell_two_message(message.chat.id, message.message_id)
            await state.clear()
            return True

        else:
            await message.delete()
            await edit_text(
                'Кількість має бути в цифрах',
                keyboard=None,
                message_id=message.message_id - 1,
                chat_id=message.chat.id
            )
            return False


cart_widget = CartWidgets()
