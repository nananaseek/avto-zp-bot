from aiogram import types

from src.app.cart.services.cart import cart_service
from src.app.cart.services.order import order_service
from src.app.product.services.product import product_service
from src.settings.config import settings


class InvoicePay:
    PAYMENT_TOKEN = settings.PAYMENT_TOKEN

    def __init__(self):
        self.item_count = 0
        self.all_price = 10000
        self.register_check = {'check_id': 0}

    def _price(self, cart):
        items = []
        for product in cart:
            price = f'{float(product['new_price']) * float(product['takes_by_user'])}'.replace('.', '')
            text = f'{product['name']} x {product["takes_by_user"]}шт.'
            items.append(types.LabeledPrice(label=text, amount=int(price) * 10))
            self.item_count += 1
            self.all_price += int(price) * 10

        return items

    def _shipping(self) -> dict[str, types.ShippingOption]:
        teleport_amount = 1000000 if self.item_count >= 3 else 1000000 * 0.01
        nova_amount = (self.all_price + (self.all_price * 0.20)) if self.item_count >= 3 else self.all_price
        ukr_amount = self.all_price

        teleport_shipping = types.ShippingOption(
            id='teleporter',
            title='Всемирный* телепорт',
            prices=[types.LabeledPrice(label='Телепорт', amount=teleport_amount)]
        )
        nova_pochta = types.ShippingOption(
            id='NovaPochta',
            title='Доставка через нову пошту',
            prices=[types.LabeledPrice(label='Посилка', amount=nova_amount)]
        )
        ukr_pochta = types.ShippingOption(
            id='UkrPochta',
            title='Доставка через Укрпошту',
            prices=[types.LabeledPrice(label='Посилка', amount=ukr_amount)]
        )
        none_shipping = types.ShippingOption(
            id='None',
            title='Без доставки',
            prices=[types.LabeledPrice(label='Без доставки', amount=0)]
        )

        return {
            'teleport': teleport_shipping,
            'nova': nova_pochta,
            'ukr': ukr_pochta,
            'none_shipping': none_shipping
        }

    async def __call__(
            self,
            cart,
            message: types.Message,
            photo_height,
            photo_width,
            picture=None,
            user_id=None,
            *args,
            **kwargs
    ):
        self.register_check['user_id'] = user_id or message.from_user.id
        self.register_check['chat_id'] = message.chat.id

        await message.answer_invoice(
            title='Оплатити покупки',
            description='тестовий опис корзини (це треба змінити)',
            provider_token=self.PAYMENT_TOKEN,
            currency='uah',
            photo_url=f'https://picsum.photos/{photo_width}/{photo_height}',
            photo_height=photo_height,
            photo_width=photo_width,
            need_name=True,
            need_phone_number=True,
            need_shipping_address=True,
            is_flexible=True,  # True If you need to set up Shipping Fee
            prices=self._price(cart),
            payload='huy',
            start_parameter='huy'
        )

    def reg_shipping_method(self):
        async def _pay_handler(pre_checkout_query: types.PreCheckoutQuery):
            data = await cart_service.carts(pre_checkout_query.from_user.id)
            for item in data:
                is_correct = await product_service.buy_product(item['id'], int(item['takes_by_user']))
                if not is_correct:
                    return await pre_checkout_query.answer(
                        ok=False,
                        error_message=f'Оновіть корзину, продукта {item['name']} вже не має на складі'
                    )
            self.register_check['product'] = data
            await pre_checkout_query.answer(True)

        async def _shipping_method(shipping_query: types.ShippingQuery):
            shipping_method = self._shipping()
            shipping_options = []
            countries = ['UA']
            if shipping_query.shipping_address.country_code not in countries:
                return await shipping_query.answer(
                    ok=False,
                    error_message='Доставка відбувається тільки в україні'
                )

            if shipping_query.shipping_address.country_code == 'UA':
                shipping_options.append(shipping_method['nova'])
                shipping_options.append(shipping_method['ukr'])

            city = ['Чернівці']
            if shipping_query.shipping_address.city in city:
                shipping_options.append(shipping_method['teleport'])

            shipping_options.append(shipping_method['none_shipping'])
            await shipping_query.answer(ok=True, shipping_options=shipping_options)

        async def _successful_message(message: types.Message):
            address = (f'Місто: {message.successful_payment.order_info.shipping_address.city}'
                       f'Область: {message.successful_payment.order_info.shipping_address.state}'
                       f'Адреса: {message.successful_payment.order_info.shipping_address.street_line1}'
                       f'Індекс: {message.successful_payment.order_info.shipping_address.post_code}')

            self.register_check['address'] = address
            self.register_check['contact'] = message.successful_payment.order_info.phone_number
            self.register_check['username'] = message.successful_payment.order_info.name
            self.register_check['shipping_method'] = message.successful_payment.shipping_option_id

            await order_service.save_check(**self.register_check)
            await cart_service.delete_all_carts(message.from_user.id)

            await message.answer('Ваше замовлення оформленно\n'
                                 'Вам надійде повідомлення коли адміністратор обробить замовлення')

        return {
            'pre_checkout': _pay_handler,
            'shipping_query': _shipping_method,
            'successful_message': _successful_message
        }


invoice = InvoicePay()
