import asyncio
import logging
from typing import Callable, Coroutine, Any, TypeVar, List, Union, Optional

from aiogram import Dispatcher, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from pydantic import BaseModel

from src.app.cart.services.cart import cart_service, CartService
from src.app.cart.services.cart_widgets import CartWidgets, cart_widget
from src.app.cart.state.cart import ChooseState

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class ProductCard:
    def __init__(
            self,
            data: list,
            carousel: bool = False,
            callback_startswith: str = 'item-page_',
            page_separator: str = '/',
            dp: Dispatcher | Router | None = None,
    ):
        """
        Example: paginator = Paginator(data=product)

        :param data: An iterable object that stores an InlineKeyboardButton.
        :param callback_startswith: What should callback_data begin with in handler pagination. Default = 'page_'.
        :param page_separator: Separator for page numbers. Default = '/'.
        """
        self.dp = dp
        self.data = data
        self.carousel = carousel
        self.page_separator = page_separator
        self._startswith = callback_startswith
        self.current_page = 0

    """
    Class for pagination's in aiogram inline keyboards
    """

    async def __call__(
            self,
            user_id,
            *args,
            **kwargs
    ) -> dict:
        """
        Example:

        await message.answer(
            text='Some menu',
            reply_markup=paginator()
        )

        :return: InlineKeyboardMarkup
        """
        current_page = self.current_page
        logging.debug(current_page)
        product = self._get_item(
            self.data,
            current_page
        )
        # logging.debug(product)
        discount = self._get_price(product)

        text = (f'Назва продукту: {product['name']} \n'
                f'Опис продукту: {product['description']}\n'
                f'Ціна: {discount}\n'
                f'Кількість на складі: {product['quantity']}шт')

        if self.carousel:
            paginations = self._get_paginator(
                counts=len(self.data),
                page=current_page,
                page_separator=self.page_separator,
                startswith=self._startswith
            )
        else:
            paginations = []

        widgets = await self.get_cart_widget(product_id=product['id'], user_id=user_id)

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[widgets, paginations])

        if self.dp:
            self.paginator_handler()
            self.widgets_handler()

        return {'photo': product['image'], 'caption': text, 'reply_markup': keyboard}

    def _get_navigate(self, current_page):
        if current_page == 'next':
            self.current_page += 1
        elif current_page == 'back':
            self.current_page -= 1

    def _get_item(
            self,
            data: Union[
                List[SchemaType],
                SchemaType
            ],
            current_item: int
    ) -> dict:
        if self.carousel:
            logging.debug(len(data))
            return data[current_item].model_dump()
        else:
            return data.model_dump()

    @staticmethod
    def _get_price(product):
        if product['discount'] is None:
            return product['price']
        else:
            new_price = product['price'] - (product['price'] * product['discount'] / 100)
            return f'<s>{product['price']}₴</s> {new_price:.2f}₴'

    @staticmethod
    def _item_from_cart(cart: list, uuid: str) -> Optional[dict]:
        if len(cart) > 0:
            for item in cart:
                if item['id'] == uuid:
                    return item
        else:
            return None

    @staticmethod
    def _get_paginator(
            counts: int,
            page: int,
            page_separator: str = '/',
            startswith: str = 'item-page_'
    ) -> list[types.InlineKeyboardButton]:
        """
        :param counts: Counts total buttons.
        :param page: Current page.
        :param page_separator: Separator for page numbers. Default = '/'.
        :return: Page control line buttons.
        """
        counts -= 1

        paginations = []

        if page > 0:
            paginations.append(
                types.InlineKeyboardButton(
                    text='⬅️',
                    callback_data=f'{startswith}back'
                ),
            )
        paginations.append(
            types.InlineKeyboardButton(
                text=f'{page + 1}{page_separator}{counts + 1}',
                callback_data='pass'
            ),
        )
        if counts > page:
            paginations.append(
                types.InlineKeyboardButton(
                    text='➡️',
                    callback_data=f'{startswith}next'
                )
            )
        return paginations

    @staticmethod
    async def get_cart_widget(user_id: int, product_id: str) -> list:
        widgets = []
        cart_item = await cart_service.get_product_from_cart(user_id, product_id)
        if cart_item is None:
            widgets.append(
                types.InlineKeyboardButton(
                    text='Додати до корзини',
                    callback_data=f'card-to-cart_{product_id}'
                )
            )
        else:
            widgets.append(
                types.InlineKeyboardButton(
                    text='+1',
                    callback_data=f'card-increase_{cart_item['id']}'
                )
            )
            widgets.append(
                types.InlineKeyboardButton(
                    text=f'✏️ {cart_item['takes_by_user']}шт.',
                    callback_data=f'card-choose-amount_{cart_item['id']}'
                )
            )
            widgets.append(
                types.InlineKeyboardButton(
                    text='-1',
                    callback_data=f'card-decrease_{cart_item['id']}'
                )
            )
        return widgets

    @staticmethod
    async def update_message(call: CallbackQuery, data):
        await call.message.edit_media(
            InputMediaPhoto(
                media=data['photo'],
                caption=data['caption']
            ),
            reply_markup=data['reply_markup']
        )

    def widgets_handler(self):
        """
        Example:

        args, kwargs = paginator.paginator_handler()

        dp.register_callback_query_handler(*args, **kwargs)

        :return: Data for register handler pagination.
        """

        async def _to_cart(call: CallbackQuery):
            added = await cart_widget.add_to_cart(call)
            if added:
                await self.update_message(
                    call,
                    await self.__call__(user_id=call.from_user.id)
                )

        async def _increase_item(call: CallbackQuery):
            increase = await cart_widget.increase_cart_item(call)
            if increase:
                await self.update_message(
                    call,
                    await self.__call__(user_id=call.from_user.id)
                )

        async def _choose_amount(call: CallbackQuery, state: FSMContext):
            await cart_widget.choose_amount(call, state)
            await state.update_data(call=call)

        async def _get_amount(message: Message, state: FSMContext):
            get_text = await cart_widget.get_amount(message, state)
            if get_text:
                data = await state.get_data()
                await self.update_message(
                    data['call'],
                    await self.__call__(user_id=message.from_user.id)
                )
                await state.clear()

        async def _decrease(call: CallbackQuery):
            decreases = await cart_widget.decrease_cart_item(call)
            if decreases:
                await self.update_message(
                    call,
                    await self.__call__(user_id=call.from_user.id)
                )

        widgets_handler = {
            _increase_item: F.data.startswith('card-increase_'),
            _to_cart: F.data.startswith('card-to-cart_'),
            _choose_amount: F.data.startswith('card-choose-amount_'),
            _decrease: F.data.startswith('card-decrease_')
        }

        # self.dp.callback_query.register(
        #     _increase_item,
        #     F.data.startswith('increase_'),
        # )
        for func, filter_key in widgets_handler.items():
            self.dp.callback_query.register(
                func,
                filter_key,
            )
        self.dp.message.register(
            _get_amount,
            ChooseState.card_amount,
            F.text
        )

    def paginator_handler(self) -> tuple[Callable[[CallbackQuery, FSMContext], Coroutine[Any, Any, None]], F]:
        """
        Example:

        args, kwargs = paginator.paginator_handler()

        dp.register_callback_query_handler(*args, **kwargs)

        :return: Data for register handler pagination.
        """

        async def _page(call: types.CallbackQuery, state: FSMContext):
            current_page = call.data.split('_')[-1]
            self._get_navigate(current_page)
            data = await self.__call__(current_page=self.current_page, user_id=call.from_user.id)

            await call.message.edit_media(
                InputMediaPhoto(
                    media=data['photo'],
                    caption=data['caption']
                ),
                reply_markup=data['reply_markup']
            )
            # await state.set_state()
            # await state.update_data({f'last_page_{self._startswith}': page})

        if not self.dp:
            return _page, F.data.startswith(self._startswith)
        else:
            self.dp.callback_query.register(
                _page,
                F.data.startswith(self._startswith),
            )
