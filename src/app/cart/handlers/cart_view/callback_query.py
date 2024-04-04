import logging

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.app.admin_panel.states.admin_panel import AdminPanel
from src.app.category.services.category import category_service
from src.app.category.utils import category_utils
from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_data, save_product, change_product_from_queryset, \
    send_product_list, change_cart_product
from src.app.product.services.product import product_service
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards, \
    inline_pagination
from src.app.product.states.add_product import AddProductState
from src.core.utils.dell_message import dell_target_message
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


@router.callback_query(F.data.startswith('add-to-cart_'))
async def add_to_cart(query: CallbackQuery):
    product_id = query.data.split('_')[1]
    is_added = await cart_service.add_product_to_cart(query.from_user.id, product_id)
    if is_added:
        product = await cart_service.get_product_from_cart(query.from_user.id, product_id)
        await change_cart_product(product, query.message, True)
        await query.answer('Одиницю товару додано')
    else:
        await query.answer('Товар неможливо додати')


@router.callback_query(F.data.startswith('minus-to-cart_'))
async def minus_product_cart(query: CallbackQuery):
    product_id = query.data.split('_')[1]
    is_delete = await cart_service.delete_product_cart(query.from_user.id, product_id)
    if is_delete:
        await query.message.delete()
        await query.answer('Товар видалено')
    else:
        product = await cart_service.get_product_from_cart(query.from_user.id, product_id)
        await change_cart_product(product, query.message, True)
        await query.answer('Видалено одиницю товару')


@router.callback_query(F.data.startswith('close-cart_'))
async def minus_product_cart(query: CallbackQuery):
    await query.message.delete()
