from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.app.cart.state.cart import ChooseState
from src.app.cart.utils.product_to_cache import get_product_to_cache

from src.app.product.handlers.utils.product import change_cart_product
from src.core.utils.dell_message import dell_two_message
from src.app.cart.services.cart import cart_service

router = Router()


@router.callback_query(F.data.startswith('cart-item_'))
async def get_item(query: CallbackQuery):
    product_id = query.data.split('_')[1]
    product = await cart_service.get_product_from_cart(query.from_user.id, product_id)
    if product is None:
        await query.message.answer('Ваша сесія закінчена, додайте продукти заново')
    else:
        await change_cart_product(product, query.message)


@router.callback_query(F.data.startswith('increase_'))
async def add_to_cart(query: CallbackQuery):
    product_id = query.data.split('_')[1]
    is_added = await cart_service.add_product_to_cart(query.from_user.id, product_id, )
    if is_added:
        product = await cart_service.get_product_from_cart(query.from_user.id, product_id)
        await change_cart_product(product, query.message, True)
        await query.answer('Одиницю товару додано')
    elif is_added is None:
        is_add = await get_product_to_cache(product_id, query.from_user.id)
        await query.answer(
            'Товар додано до корзини'
            if is_add else
            'Неможливо додати ще товару бо такої кількості не має на складі'
        )
    else:
        await query.answer('Товар неможливо додати')


@router.callback_query(F.data.startswith('choose-amount_'))
async def choose_amount(query: CallbackQuery, state: FSMContext):
    product_id = query.data.split('_')[1]
    await state.clear()
    await query.message.answer('Скільки ви хочете штук')
    await state.set_state(ChooseState.amount)
    await state.update_data(product_id=product_id, message=query.message)


@router.callback_query(F.data.startswith('decrease_'))
async def minus_product_cart(query: CallbackQuery):
    product_id = query.data.split('_')[1]
    is_delete = await cart_service.delete_product_cart(query.from_user.id, product_id)
    if is_delete:
        await query.message.delete()
        await query.answer('Товар видалено')
    elif is_delete is None:
        await query.answer('Товару не має в корзині')
    else:
        product = await cart_service.get_product_from_cart(query.from_user.id, product_id)
        await change_cart_product(product, query.message, True)
        await query.answer('Видалено одиницю товару')


@router.callback_query(F.data == 'clean_carts')
async def clean_carts(query: CallbackQuery):
    await cart_service.delete_all_carts(query.from_user.id)
    await dell_two_message(query.message.chat.id, query.message.message_id)
    await query.answer('Корзину очищено')


@router.callback_query(F.data.startswith('close-cart_'))
async def minus_product_cart(query: CallbackQuery):
    await query.message.delete()
